from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.getenv("VAYUNET_API_URL", "http://localhost:8000/api/v1").rstrip("/")

ENDPOINTS = [
    "/health",
    "/hotspots",
    "/alerts",
    "/federation/status",
    "/cloud/status",
]

def get_json(path: str) -> object:
    url = f"{BASE_URL}{path}"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=10) as response:
        body = response.read().decode("utf-8")
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return json.loads(body)

def main() -> int:
    print(f"VayuNet smoke test target: {BASE_URL}")
    failures = 0

    for endpoint in ENDPOINTS:
        try:
            data = get_json(endpoint)
            print(f"PASS {endpoint}")
            if endpoint == "/health" and not isinstance(data, dict):
                raise RuntimeError("health response is not an object")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, RuntimeError) as exc:
            failures += 1
            print(f"FAIL {endpoint}: {exc}")

    if failures:
        print(f"Smoke test failed: {failures} endpoint(s) unavailable.")
        return 1

    print("Smoke test passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
