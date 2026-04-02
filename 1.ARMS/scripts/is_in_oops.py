import os
import json
from datetime import datetime
from dateutil import parser

PASSPORT_DIR = "../passports"


def _norm_name(x):
    return str(x).strip().lower() if x else None


def _norm_float(x):
    try:
        return float(x)
    except Exception:
        return None


def _norm_date(x):
    if x is None or x == "":
        return None
    try:
        dt = parser.parse(str(x))
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def validate_exists(lat, lon, name, date, tolerance=1e-5):
    """
    Returns:
        (True, filepath, passport_json)
        (False, None, None)
    """

    if not os.path.exists(PASSPORT_DIR):
        return False, None, None

    t_lat = _norm_float(lat)
    t_lon = _norm_float(lon)
    t_name = _norm_name(name)
    t_date = _norm_date(date)

    for filename in os.listdir(PASSPORT_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(PASSPORT_DIR, filename)

        try:
            with open(filepath, "r") as f:
                passport = json.load(f)
        except Exception:
            continue

        try:
            patch = passport.get("platform", {}).get("patch", {})
            dep = patch.get("deployment", {})

            s_lat = _norm_float(dep.get("latitude"))
            s_lon = _norm_float(dep.get("longitude"))
            s_name = _norm_name(patch.get("name"))
            s_date = _norm_date(dep.get("date"))

            if (
                s_lat is not None and t_lat is not None and
                s_lon is not None and t_lon is not None and
                abs(s_lat - t_lat) < tolerance and
                abs(s_lon - t_lon) < tolerance and
                s_name == t_name and
                s_date == t_date
            ):
                return True, filepath, passport

        except Exception:
            continue

    return False, None, None