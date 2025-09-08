export default function HistoryList({ history }) {
  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-3">Verlauf</h2>
      {history.length === 0 ? (
        <p className="text-gray-500">Noch keine Anfragen.</p>
      ) : (
        <ul className="space-y-2">
          {history.map((h, idx) => (
            <li
              key={idx}
              className="p-2 bg-gray-50 rounded border flex justify-between"
            >
              <span>
                {h.city}, {h.country}
              </span>
              <span>{h.temp}°C</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
