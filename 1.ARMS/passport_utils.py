import os
import json
import random
from datetime import datetime
from dateutil import parser

# -------------------------------------------------------------------
# Time helpers
# -------------------------------------------------------------------
def now_utc():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def to_iso(x):
    if x is None or x == "" or (isinstance(x, float) and str(x) == "nan"):
        return None
    try:
        dt = parser.parse(str(x))
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


# -------------------------------------------------------------------
# String safety
# -------------------------------------------------------------------
def safe_chr(x):
    if x is None or x == "" or (isinstance(x, float) and str(x) == "nan"):
        return None
    return str(x)


# -------------------------------------------------------------------
# Mock WIGOS ID generator
# -------------------------------------------------------------------
def generate_wigos_id():
    return "".join(random.choices("0123456789abcdef", k=12))


# -------------------------------------------------------------------
# Remove null values recursively
# -------------------------------------------------------------------
def remove_nulls(x):
    if isinstance(x, dict):
        return {k: remove_nulls(v) for k, v in x.items() if v is not None}
    elif isinstance(x, list):
        return [remove_nulls(v) for v in x if v is not None]
    return x


# -------------------------------------------------------------------
# Create new passport
# -------------------------------------------------------------------
def create_passport(filepath, json_obj):
    with open(filepath, "w") as f:
        json.dump(json_obj, f, indent=2)
    print(f"created: {os.path.basename(filepath)}")


# -------------------------------------------------------------------
# Update existing passport
# -------------------------------------------------------------------
def update_passport(filepath, csv_row, config):

    with open(filepath, "r") as f:
        passport = json.load(f)

    # ---------------------------------------------------------------
    # 1. Apply CSV updates
    # ---------------------------------------------------------------
    update_fields = {
        "name": safe_chr(csv_row.get("station_name")),
        "latitude": csv_row.get("deploy_latitude"),
        "longitude": csv_row.get("deploy_longitude"),
        "date": to_iso(csv_row.get("deploy_date_time")),
        "endDate": to_iso(csv_row.get("recover_date_time")),
    }

    if "platform" in passport and "patch" in passport["platform"]:
        patch = passport["platform"]["patch"]

        if "deployment" in patch:
            if update_fields["date"]:
                patch["deployment"]["date"] = update_fields["date"]

            if update_fields["latitude"] is not None:
                patch["deployment"]["latitude"] = update_fields["latitude"]

            if update_fields["longitude"] is not None:
                patch["deployment"]["longitude"] = update_fields["longitude"]

        if "retrieval" in patch and update_fields["endDate"]:
            patch["retrieval"]["endDate"] = update_fields["endDate"]

        if update_fields["name"]:
            patch["name"] = update_fields["name"]

    # ---------------------------------------------------------------
    # 2. Apply CONFIG updates
    # ---------------------------------------------------------------
    passport = apply_config_updates(passport, config)

    # ---------------------------------------------------------------
    # Save
    # ---------------------------------------------------------------
    with open(filepath, "w") as f:
        json.dump(passport, f, indent=2)

    print(f"updated: {os.path.basename(filepath)}")


# -------------------------------------------------------------------
# Build full passport (NEW)
# -------------------------------------------------------------------
def build_full_passport(row, config, wigos_id):

    return {
        "meta": {
            "schemaVersion": config["meta"]["schemaVersion"],
            "sourceText": config["meta"]["sourceText"],
            "ingestionMethodId": config["meta"]["ingestionMethodId"],
            "contactId": config["ingestion"]["contact_id"],
            "observedAt": now_utc()
        },

        "options": config["options"],

        "platform": {
            "match": {
                "wigosId": wigos_id
            },

            "patch": {
                "name": safe_chr(row.get("station_name")),

                "deployment": {
                    "date": to_iso(row.get("deploy_date_time")),
                    "latitude": row.get("deploy_latitude"),
                    "longitude": row.get("deploy_longitude"),

                    "method": {
                        "code": config["defaults"]["deployment"]["method_code"]
                    },

                    "maxWaterDepth": config["defaults"]["deployment"]["maxWaterDepth"],
                    "elevation": config["defaults"]["deployment"]["elevation"],

                    "ship": {
                        "imoNumber": config["defaults"]["deployment"]["ship_imo"]
                    }
                },

                "retrieval": {
                    "match": {
                        "wigosId": wigos_id
                    },
                    "endDate": to_iso(row.get("recover_date_time"))
                }
            }
        },

        "sensorSetups": [
            {
                "match": {},
                "data": {
                    "create": {
                        "variable": {"code": s["variable_code"]},
                        "sensorModel": {"name": s["sensor_model"]}
                    }
                }
            }
            for s in config["defaults"]["sensors"]
        ],

        "contactContributions": [],
        "agencyContributions": []
    }


def apply_config_updates(passport, config):

    # ---------------------------------------------------------------
    # Meta updates
    # ---------------------------------------------------------------
    if "meta" in passport:
        passport["meta"]["schemaVersion"] = config["meta"]["schemaVersion"]
        passport["meta"]["sourceText"] = config["meta"]["sourceText"]
        passport["meta"]["ingestionMethodId"] = config["meta"]["ingestionMethodId"]
        passport["meta"]["contactId"] = config["ingestion"]["contact_id"]

    # ---------------------------------------------------------------
    # Options
    # ---------------------------------------------------------------
    passport["options"] = config["options"]

    # ---------------------------------------------------------------
    # Agency (replace fully)
    # ---------------------------------------------------------------
    passport["agencyContributions"] = [
        {
            "agencyId": config["agency"]["id"],
            "roles": config["agency"]["roles"]
        }
    ]

    # ---------------------------------------------------------------
    # Contact contributions (rebuild from config)
    # ---------------------------------------------------------------
    passport["contactContributions"] = [
        {
            "contactId": c["id"],
            "roles": [c["role"]]
        }
        for c in config["contacts"].values()
    ]

    # ---------------------------------------------------------------
    # Sensors (replace completely)
    # ---------------------------------------------------------------
    passport["sensorSetups"] = [
        {
            "match": {},
            "data": {
                "create": {
                    "variable": {"code": s["variable_code"]},
                    "sensorModel": {"name": s["sensor_model"]}
                }
            }
        }
        for s in config["defaults"]["sensors"]
    ]

    return passport