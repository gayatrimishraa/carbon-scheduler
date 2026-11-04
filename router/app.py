import json
import os
import csv
import time
import uuid
import boto3
from datetime import datetime, timezone

# ── Cold-start flag ──────────────────────────────────────────────────────────
_cold_start = True

# ── Load carbon replay data at init (runs once per container) ────────────────
_carbon = {}   # {(region, hour_index): gco2_per_kwh}

def _load_carbon():
    path = os.path.join(os.path.dirname(__file__), "carbon_replay.csv")
    with open(path) as f:
        for row in csv.DictReader(f):
            key = (row["region"], int(row["hour_index"]))
            _carbon[key] = float(row["gco2_per_kwh"])

_load_carbon()

# ── Constants ────────────────────────────────────────────────────────────────
REGIONS = ["ap-south-1", "eu-north-1", "us-east-1"]
HOME    = "ap-south-1"

# Relative cost factor per region (us-east-1 = 1.0 baseline)
COST_FACTOR = {
    "us-east-1":  1.00,
    "eu-north-1": 1.08,
    "ap-south-1": 1.10,
}

# Cloud Carbon Footprint methodology: 0.00039 kW/GB, AWS average PUE 1.67
POWER_COEFF = 0.00039
PUE         = 1.67
MEMORY_GB   = 128 / 1024

# DynamoDB
_ddb    = boto3.resource("dynamodb", region_name="ap-south-1")
_tbl_rs = _ddb.Table("region_state")
_tbl_rq = _ddb.Table("requests")

# Worker ARNs from env
WORKER_ARNS = json.loads(os.environ["WORKER_ARNS"])

# Secret token
SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "")

# Round-robin counter (in-memory, resets on cold start — good enough)
_rr_index = 0


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_carbon(region, sim_hour):
    hour = sim_hour % 48          # replay wraps at 48h
    return _carbon.get((region, hour), 80.0)

def _cold_penalty(last_invoked_str):
    """0.0 if invoked < 5 min ago, linear to 1.0 at 30 min."""
    try:
        last = datetime.fromisoformat(last_invoked_str)
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        age_min = (datetime.now(timezone.utc) - last).total_seconds() / 60
    except Exception:
        age_min = 999
    if age_min < 5:
        return 0.0
    if age_min >= 30:
        return 1.0
    return (age_min - 5) / 25

def _normalize(values):
    """Min-max normalize a dict {region: value} → {region: 0..1}."""
    mn = min(values.values())
    mx = max(values.values())
    if mx == mn:
        return {r: 0.0 for r in values}
    return {r: (v - mn) / (mx - mn) for r, v in values.items()}

def _estimate_gco2(duration_ms, carbon_intensity):
    duration_s = duration_ms / 1000
    energy_kwh = duration_s * MEMORY_GB *