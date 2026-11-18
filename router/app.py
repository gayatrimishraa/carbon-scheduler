import json
import os
import csv
import time
import uuid
import boto3
from datetime import datetime, timezone

# ── Cold-start flag ──────────────────────────────────────────────────────────
_cold_start = True

# ── Load carbon replay data at init ─────────────────────────────────────────
_carbon = {}

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

COST_FACTOR = {
    "us-east-1":  1.00,
    "eu-north-1": 1.08,
    "ap-south-1": 1.10,
}

POWER_COEFF = 0.00039
PUE         = 1.67
MEMORY_GB   = 128 / 1024

_ddb    = boto3.resource("dynamodb", region_name="ap-south-1")
_tbl_rs = _ddb.Table("region_state")
_tbl_rq = _ddb.Table("requests")

WORKER_ARNS  = json.loads(os.environ["WORKER_ARNS"])
SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "")

_rr_index = 0

# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_carbon(region, sim_hour):
    hour = sim_hour % 48
    return _carbon.get((region, hour), 80.0)

def _cold_penalty(last_invoked_str):
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
    mn = min(values.values())
    mx = max(values.values())
    if mx == mn:
        return {r: 0.0 for r in values}
    return {r: (v - mn) / (mx - mn) for r, v in values.items()}

def _estimate_gco2(duration_ms, carbon_intensity):
    duration_s = duration_ms / 1000
    energy_kwh = (duration_s * MEMORY_GB * POWER_COEFF * PUE) / 3600
    return energy_kwh * carbon_intensity * 1000

# ── Region state from DynamoDB ───────────────────────────────────────────────

def _get_region_state():
    state = {}
    for region in REGIONS:
        try:
            resp = _tbl_rs.get_item(Key={"region": region})
            item = resp.get("Item", {})
            state[region] = {
                "ewma_latency": float(item.get("ewma_latency_ms", 300)),
                "last_invoked": item.get("last_invoked", "2000-01-01T00:00:00+00:00"),
            }
        except Exception:
            state[region] = {
                "ewma_latency": 300,
                "last_invoked": "2000-01-01T00:00:00+00:00",
            }
    return state

def _update_region_state(region, latency_ms):
    try:
        resp = _tbl_rs.get_item(Key={"region": region})
        old_ewma = float(resp.get("Item", {}).get("ewma_latency_ms", latency_ms))
        new_ewma = 0.3 * latency_ms + 0.7 * old_ewma
        _tbl_rs.put_item(Item={
            "region": region,
            "ewma_latency_ms": str(round(new_ewma, 2)),
            "last_invoked": datetime.now(timezone.utc).isoformat(),
        })
    except Exception:
        pass

# ── Scheduling policies ──────────────────────────────────────────────────────

def _select_home(sim_hour, state):
    return HOME

def _select_round_robin(sim_hour, state):
    global _rr_index
    region = REGIONS[_rr_index % len(REGIONS)]
    _rr_index += 1
    return region

def _select_carbon_only(sim_hour, state):
    return min(REGIONS, key=lambda r: _get_carbon(r, sim_hour))

def _select_multi_objective(sim_hour, state,
                             w_carbon=0.4, w_latency=0.3,
                             w_cold=0.2, w_cost=0.1):
    carbon  = {r: _get_carbon(r, sim_hour) for r in REGIONS}
    latency = {r: state[r]["ewma_latency"] for r in REGIONS}
    cold    = {r: _cold_penalty(state[r]["last_invoked"]) for r in REGIONS}
    cost    = {r: COST_FACTOR[r] for r in REGIONS}

    nc = _normalize(carbon)
    nl = _normalize(latency)
    nco = cold
    nct = _normalize(cost)

    scores = {
        r: w_carbon * nc[r] + w_latency * nl[r] +
           w_cold * nco[r] + w_cost * nct[r]
        for r in REGIONS
    }
    return min(scores, key=scores.get)

POLICIES = {
    "home":            _select_home,
    "always-home":     _select_home,
    "round-robin":     _select_round_robin,
    "carbon-only":     _select_carbon_only,
    "multi-objective": _select_multi_objective,
}

# ── Worker invocation ────────────────────────────────────────────────────────

def _invoke_worker(region, payload):
    client = boto3.client("lambda", region_name=region)
    arn    = WORKER_ARNS[region]
    t0     = time.time()
    resp   = client.invoke(
        FunctionName=arn,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload).encode(),
    )
    duration_ms = (time.time() - t0) * 1000
    result = json.loads(resp["Payload"].read())
    was_cold = result.get("was_cold", False)
    return duration_ms, was_cold, result

# ── Lambda handler ───────────────────────────────────────────────────────────

def lambda_handler(event, context):
    global _cold_start

    # CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "content-type,x-scheduler-token,x-secret-token,authorization",
            },
            "body": "",
        }

    # Auth
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    token   = headers.get("x-scheduler-token") or headers.get("x-secret-token", "")
    if SECRET_TOKEN and token != SECRET_TOKEN:
        return {
            "statusCode": 401,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Unauthorized"}),
        }

    # Parse body
    try:
        body = json.loads(event.get("body") or "{}")
    except Exception:
        body = {}

    policy   = body.get("policy", "multi-objective").lower()
    sim_hour = int(body.get("sim_hour", 0))
    run_id   = body.get("run_id", str(uuid.uuid4()))
    payload  = body.get("payload", {"task": "default"})

    # This invocation's cold-start flag
    this_cold = _cold_start
    _cold_start = False

    # Get region state and select region
    state  = _get_region_state()
    fn     = POLICIES.get(policy, _select_multi_objective)
    region = fn(sim_hour, state)

    # Invoke worker
    try:
        duration_ms, was_cold, worker_result = _invoke_worker(region, payload)
    except Exception as e:
        return {
            "statusCode": 502,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }

    # Update EWMA latency
    _update_region_state(region, duration_ms)

    # Carbon estimate
    carbon_intensity = _get_carbon(region, sim_hour)
    estimated_gco2   = _estimate_gco2(duration_ms, carbon_intensity)

    # Log to DynamoDB
    try:
        _tbl_rq.put_item(Item={
            "request_id":       run_id,
            "timestamp":        datetime.now(timezone.utc).isoformat(),
            "policy":           policy,
            "selected_region":  region,
            "sim_hour":         sim_hour,
            "latency_ms":       str(round(duration_ms, 2)),
            "was_cold":         was_cold,
            "estimated_gco2":   str(round(estimated_gco2, 8)),
            "carbon_intensity": str(carbon_intensity),
        })
    except Exception:
        pass

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({
            "request_id":       run_id,
            "policy":           policy,
            "selected_region":  region,
            "sim_hour":         sim_hour,
            "latency_ms":       round(duration_ms, 2),
            "was_cold":         was_cold,
            "estimated_gco2":   round(estimated_gco2, 8),
            "carbon_intensity": carbon_intensity,
            "worker_result":    worker_result,
        }),
    }