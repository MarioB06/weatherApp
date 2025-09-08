import { useState } from "react";

export default function AlertForm() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);

  const sendAlert = async () => {
    try {
      const res = await fetch("http://localhost:8000/alert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ msg: "Fehler beim Senden" });
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-3">Alert speichern</h2>
      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Warnung eingeben..."
        />
        <button
          onClick={sendAlert}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Senden
        </button>
      </div>
      {response && <p className="mt-2 text-sm">{response.msg}</p>}
    </div>
  );
}
