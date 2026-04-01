import os
import pandas as pd

from passport_utils import (
    generate_wigos_id,
    create_passport,
    update_passport,
    build_full_passport,
    safe_chr
)

# -------------------------------------------------------------------
# Load data + config
# -------------------------------------------------------------------
arms = pd.read_csv("ETN_ARMS_EXPORT/deployments_ARMS_update.csv")

import json
with open("config/config_passports.json", "r") as f:
    config = json.load(f)

# -------------------------------------------------------------------
# Output directory
# -------------------------------------------------------------------
OUTPUT_DIR = "passports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Main loop
# -------------------------------------------------------------------
for _, row in arms.iterrows():

    deployment_id = safe_chr(row.get("deployment_id"))

    if not deployment_id:
        print("Skipping row: missing deployment_id")
        continue

    filepath = os.path.join(
        OUTPUT_DIR,
        f"etn_deployment_id_{deployment_id}.json"
    )

    # ---------------------------------------------------------------
    # CASE 1: Passport exists → update
    # ---------------------------------------------------------------
    if os.path.exists(filepath):
        update_passport(filepath, row.to_dict(), config)
        continue

    # ---------------------------------------------------------------
    # CASE 2: New passport → create
    # ---------------------------------------------------------------
    wigos_id = generate_wigos_id()

    json_obj = build_full_passport(row, config, wigos_id)

    create_passport(filepath, json_obj)