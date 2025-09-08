import { useState } from "react";

export default function WeatherSearch({ onResult }) {
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const fetchWeather = async () => {
    setError("");
    try {
      const res = await fetch(`http://localhost:8000/weather?city=${city}`);
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Fehler beim Abrufen");
      }
      const data = await res.json();
      setResult(data);
      onResult(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-3">Suche Wetter</h2>
      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Stadt eingeben..."
        />
        <button
          onClick={fetchWeather}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Suchen
        </button>
      </div>
      {error && <p className="text-red-500 mt-2">{error}</p>}
      {result && (
        <div className="mt-3 p-3 bg-blue-50 rounded">
          <p>
            🌍 {result.city}, {result.country}
          </p>
          <p>🌡 {result.temp}°C (gefühlt {result.feels_like}°C)</p>
          <p>☁ {result.condition}</p>
        </div>
      )}
    </div>
  );
}
