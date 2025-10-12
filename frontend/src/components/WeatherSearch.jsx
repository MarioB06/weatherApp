import { useState } from "react";
import { fetchWeather } from "../lib/api";

export default function WeatherSearch({ onResult }) {
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const fetchData = async () => {
    setError("");
    if (!city) {
      setError("Bitte Stadt eingeben");
      return;
    }
    try {
      const data = await fetchWeather(city);
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
          onClick={fetchData}
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
          {result.timestamp && (
            <p className="text-sm text-gray-600">
              🕒 {new Date(result.timestamp).toLocaleString()}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
