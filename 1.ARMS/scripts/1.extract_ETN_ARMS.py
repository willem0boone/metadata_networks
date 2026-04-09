import requests
import json
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

url = "https://opencpu.lifewatch.be/library/etnservice/R/get_acoustic_deployments/json"

payload = {
    "credentials": {
        "username": os.getenv("ETN_USER"),
        "password": os.getenv("ETN_PWD")
    },
    "acoustic_project_code": ["bpns"]
}

response = requests.post(
    url,
    data=json.dumps(payload),
    headers={"Content-Type": "application/json"}
)

print(response.status_code)

data = response.json()

filtered = [
    d for d in data
    if "emobon" in d.get("station_name", "").lower()
]

print(len(filtered))
pprint(filtered)

with open("../etn_arms_export/deployments_ARMS.json", 'w') as f:
    json.dump(filtered, f, indent=4, sort_keys=True, ensure_ascii=False)

