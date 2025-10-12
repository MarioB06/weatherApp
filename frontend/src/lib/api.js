const API_BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(
  /\/$/,
  ""
);

async function handleResponse(response) {
  if (!response.ok) {
    let detail = "Unbekannter Fehler";
    try {
      const payload = await response.json();
      detail = payload.detail || JSON.stringify(payload);
    } catch (err) {
      detail = response.statusText || detail;
    }
    throw new Error(detail);
  }
  return response.json();
}

export async function fetchWeather(city) {
  const url = `${API_BASE_URL}/weather?city=${encodeURIComponent(city)}`;
  const response = await fetch(url);
  return handleResponse(response);
}

export async function fetchHistory() {
  const response = await fetch(`${API_BASE_URL}/history`);
  return handleResponse(response);
}

export async function postAlert(payload) {
  const response = await fetch(`${API_BASE_URL}/alert`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse(response);
}

export async function postHistory(entry) {
  const response = await fetch(`${API_BASE_URL}/history`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(entry),
  });
  return handleResponse(response);
}

export { API_BASE_URL };
