import requests
import json

base_url = "https://www.ocean-ops.org/api/1/data/platform"


date_threshold = "2026-01-01"

# Example assumes a date field like 'lastUpdate' (adjust if needed)
exp_filter = f"""[
    "insertDate > '{date_threshold}'"
]"""

response = requests.get(
    base_url,
    params={"exp": exp_filter}
)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)