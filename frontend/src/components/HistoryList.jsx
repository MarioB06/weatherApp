export default function HistoryList({ history, loading, error }) {
  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-3">Verlauf</h2>
      {loading && <p className="text-gray-500">Lade Verlauf...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {!loading && history.length === 0 ? (
        <p className="text-gray-500">Noch keine Anfragen.</p>
      ) : (
        <ul className="space-y-2">
          {history.map((h, idx) => (
            <li
              key={idx}
              className="p-2 bg-gray-50 rounded border flex flex-col md:flex-row md:items-center md:justify-between md:gap-4"
            >
              <span className="font-medium">
                {h.city}
                {h.country ? `, ${h.country}` : ""}
              </span>
              <span className="text-sm text-gray-500">
                {h.timestamp ? new Date(h.timestamp).toLocaleString() : ""}
              </span>
              <span className="text-blue-600">{h.temp ?? "-"}°C</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
