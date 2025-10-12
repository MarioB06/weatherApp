import { useEffect, useState } from "react";
import WeatherSearch from "./components/WeatherSearch";
import HistoryList from "./components/HistoryList";
import AlertForm from "./components/AlertForm";
import { fetchHistory } from "./lib/api";

function App() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const addToHistory = (entry) => {
    setHistory((prev) => [...prev, entry]);
  };

  useEffect(() => {
    const loadHistory = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await fetchHistory();
        setHistory(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">🌦 Weather App</h1>
      <div className="max-w-2xl mx-auto space-y-6">
        <WeatherSearch onResult={addToHistory} />
        <HistoryList history={history} loading={loading} error={error} />
        <AlertForm />
      </div>
    </div>
  );
}

export default App;
