import os
import pandas as pd
import json

from utils import (
    generate_wigos_id,  # only for temp filename now
    create_passport,
    update_passport,
    build_full_passport,
    safe_chr
)

from is_in_oops import validate_exists


OUTPUT_DIR = "../passports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

arms = pd.read_csv("../etn_arms_export/deployments_ARMS.csv")

with open("config/config_passports.json", "r") as f:
    config = json.load(f)


for _, row in arms.iterrows():

    deployment_id = safe_chr(row.get("deployment_id"))

    if not deployment_id:
        print("Skipping row: missing deployment_id")
        continue

    print(f"\nProcessing ETN: {deployment_id}")

    lat = row.get("deploy_latitude")
    lon = row.get("deploy_longitude")
    name = row.get("station_name")
    date = row.get("deploy_date_time")

    exists, filepath, passport = validate_exists(lat, lon, name, date)

    # ---------------------------------------------------------------
    # CASE 1: Exists → update
    # ---------------------------------------------------------------
    if exists:
        print(f"Match found → updating {os.path.basename(filepath)}")
        update_passport(filepath, row.to_dict(), config)
        continue

    # ---------------------------------------------------------------
    # CASE 2: New → create WITHOUT WIGOS
    # ---------------------------------------------------------------
    print("No match found → creating NEW (no WIGOS yet)")

    temp_id = generate_wigos_id()  # just for filename

    json_obj = build_full_passport(row, config, wigos_id=None)

    etn_id = deployment_id

    filename = f"ETN_{etn_id}_WIGOS_NONE.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    create_passport(filepath, json_obj)