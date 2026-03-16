import json
import requests
from config import Settings

settings = Settings()

# ----------------------------
# Endpoint - clean, safe URL
# ----------------------------
API_URL = "https://www.ocean-ops.org/api/data/passports/submissions"

headers = {
    "Content-Type": "application/json",
    "X-OceanOPS-Metadata-ID": settings.API_KEY_ID,
    "X-OceanOPS-Metadata-Token": settings.API_KEY_TOKEN
}

# ----------------------------
# Load JSON payload
# ----------------------------
payload_file = "passport.json"
with open(payload_file, "r", encoding="utf-8") as f:
    payload = json.load(f)

# Ensure dryRun is True to prevent real updates
payload.setdefault("options", {})["dryRun"] = True

# ----------------------------
# Test endpoint without updating
# ----------------------------
try:
    response = requests.post(API_URL, headers=headers, json=payload)
except requests.RequestException as e:
    print("Request failed:", e)
    exit(1)

# ----------------------------
# Output results
# ----------------------------
print("Status Code:", response.status_code)

try:
    print(json.dumps(response.json(), indent=2))
except json.JSONDecodeError:
    print(response.text)


