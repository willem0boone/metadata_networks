import requests
import json
from config import Settings

# Base API URL
BASE_URL = "https://www.ocean-ops.org/api/data"
PLATFORM_ID = "0-22000-0-6204817"  # Example: WIGOS ID of the platform
API_URL = f"{BASE_URL}/platforms/{PLATFORM_ID}"

settings = Settings()

headers = {
    "Content-Type": "application/json",
    "X-OceanOPS-Metadata-ID": settings.API_KEY_ID,
    "X-OceanOPS-Metadata-Token": settings.API_KEY_TOKEN
}

# Payload: only updating the deployment date
payload = {
    "deployment": {
        "date": "2000-01-01T00:00:00Z"
    }
}

# Send PATCH request
response = requests.patch(API_URL, headers=headers, json=payload)

# Print status and results
print("URL called:", API_URL)
print("Status Code:", response.status_code)

try:
    data = response.json()
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print(response.text)