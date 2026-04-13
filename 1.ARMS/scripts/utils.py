import os
import json
import random
from datetime import datetime
from dateutil import parser


# -------------------------------------------------------------------
# Internal helpers
# -------------------------------------------------------------------
def _now_utc():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _to_iso(x):
    if x is None or x == "" or (isinstance(x, float) and str(x) == "nan"):
        return None
    try:
        dt = parser.parse(str(x))
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


# -------------------------------------------------------------------
# Public helpers
# -------------------------------------------------------------------
def safe_chr(x):
    if x is None or x == "" or (isinstance(x, float) and str(x) == "nan"):
        return None
    return str(x)


def generate_wigos_id():
    return "".join(random.choices("0123456789abcdef", k=12))


# -------------------------------------------------------------------
# Create passport
# -------------------------------------------------------------------
def create_passport(filepath, json_obj):
    with open(filepath, "w") as f:
        json.dump(json_obj, f, indent=2)
    print(f"Created: {os.path.basename(filepath)}")


# -------------------------------------------------------------------
# Update passport (with change detection)
# -------------------------------------------------------------------
def update_passport(filepath, csv_row, config):

    print(f"Validating changes for: {os.path.basename(filepath)}")

    with open(filepath, "r") as f:
        passport = json.load(f)

    original = json.loads(json.dumps(passport))

    update_fields = {
        "name": safe_chr(csv_row.get("station_name")),
        "latitude": csv_row.get("deploy_latitude"),
        "longitude": csv_row.get("deploy_longitude"),
        "date": _to_iso(csv_row.get("deploy_date_time")),
        "endDate": _to_iso(csv_row.get("recover_date_time")),
    }

    patch = passport.get("platform", {}).get("patch", {})

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

    passport = apply_config_updates(passport, config)

    if passport == original:
        print("No changes found.")
        return

    print("Changes detected → updating file")

    with open(filepath, "w") as f:
        json.dump(passport, f, indent=2)

    print(f"Updated: {os.path.basename(filepath)}")


# -------------------------------------------------------------------
# Build new passport
# -------------------------------------------------------------------
def build_full_passport(row, config, wigos_id):

    contact_contributions, agency_contributions = build_contributions(config)

    return {
        "meta": {
            "schemaVersion": config["meta"]["schemaVersion"],
            "sourceText": config["meta"]["sourceText"],
            "ingestionMethodId": config["meta"]["ingestionMethodId"],
            "contactId": config["ingestion"]["contact_id"],
            "observedAt": _now_utc()
        },
        "options": config["options"],
        "platform": {
            "match": {
                "wigosId": wigos_id
            },
            "patch": {
                "name": safe_chr(row.get("station_name")),
                "deployment": {
                    "date": _to_iso(row.get("deploy_date_time")),
                    "latitude": row.get("deploy_latitude"),
                    "longitude": row.get("deploy_longitude"),
                },
                "retrieval": {
                    "endDate": _to_iso(row.get("recover_date_time"))
                }
            }
        },
        "sensorSetups": [],
        "contactContributions": contact_contributions,
        "agencyContributions": agency_contributions
    }


# -------------------------------------------------------------------
# Apply config updates
# -------------------------------------------------------------------
def apply_config_updates(passport, config):

    passport["meta"]["schemaVersion"] = config["meta"]["schemaVersion"]
    passport["meta"]["sourceText"] = config["meta"]["sourceText"]
    passport["meta"]["ingestionMethodId"] = config["meta"]["ingestionMethodId"]
    passport["meta"]["contactId"] = config["ingestion"]["contact_id"]

    passport["options"] = config["options"]

    # NEW: update contributions
    contact_contributions, agency_contributions = build_contributions(config)

    passport["contactContributions"] = contact_contributions
    passport["agencyContributions"] = agency_contributions

    return passport


def build_contributions(config):
    contact_contributions = []
    agency_contributions = []

    # Contacts
    for key, contact in config.get("contacts", {}).items():
        contact_contributions.append({
            "contactId": contact["id"],
            "roleId": contact["role_id"]
        })

    # Agency
    agency = config.get("agency")
    if agency:
        for role in agency.get("roles", []):
            agency_contributions.append({
                "agencyId": agency["id"],
                "role": role
            })

    return contact_contributions, agency_contributions