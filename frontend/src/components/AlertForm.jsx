import { useState } from "react";
import { postAlert } from "../lib/api";

export default function AlertForm() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);

  const sendAlert = async () => {
    if (!message.trim()) {
      setResponse({ msg: "Bitte eine Nachricht eingeben" });
      return;
    }
    try {
      const data = await postAlert({ message });
      setResponse(data);
      setMessage("");
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
