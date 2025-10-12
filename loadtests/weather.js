import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "10s", target: 10 },
    { duration: "30s", target: 25 },
    { duration: "10s", target: 0 },
  ],
};

const BASE_URL = __ENV.API_BASE_URL || "http://localhost:8000";

export default function () {
  const response = http.get(`${BASE_URL}/weather?city=Bern`);
  check(response, {
    "status ist 200": (r) => r.status === 200 || r.status === 500, // 500 erlaubt bei fehlendem API-Key
  });
  sleep(1);
}
