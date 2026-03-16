import requests
import json
from config import Settings


settings = Settings()
# Base API URL
BASE_URL = "https://www.ocean-ops.org/api/data"
ENDPOINT = "/vocab/ptf-statuses"
API_URL = BASE_URL + ENDPOINT


headers = {
    "Accept": "application/json",
    "X-OceanOPS-Metadata-ID": settings.API_KEY_ID,
    "X-OceanOPS-Metadata-Token": settings.API_KEY_TOKEN
}

# Optional query parameters
params = {
    "q": "",       # search string, leave empty to get all
    "limit": 50,   # max 200
    "offset": 0
}

# Send GET request
response = requests.get(API_URL, headers=headers, params=params)

# Print status and results
print("URL called:", response.url)
print("Status Code:", response.status_code)

try:
    data = response.json()
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print(response.text)