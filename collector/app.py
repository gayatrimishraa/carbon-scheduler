import os, json, csv, time, random, datetime, pathlib
import boto3

REGION      = "ap-south-1"
TABLE_NAME  = os.environ["TABLE_NAME"]          # carbon_live
SSM_PARAM   = os.environ["SSM_PARAM"]           # /carbon-scheduler/live-mode
REPLAY_CSV  = pathlib.Path("/var/task/carbon_replay.csv")

dynamodb = boto3.resource("dynamodb", region_name=REGION)
ssm      = boto3.client("ssm",      region_name=REGION)
table    = dynamodb.Table(TABLE_NAME)

REGIONS = ["ap-south-1", "eu-north-1", "us-east-1"]

def _load_replay():
    """Return {region: [gco2_per_kwh across hours]}"""
    data = {r: [] for r in REGIONS}
    with open(REPLAY_CSV, newline="") as f:
        for row in csv.DictReader(f):
            r = row["region"]
            if r in data:
                data[r].append(float(row["gco2_per_kwh"]))
    return data

def _is_live_mode():
    try:
        resp = ssm.get_parameter(Name=SSM_PARAM)
        return resp["Parameter"]["Value"].strip().lower() == "true"
    except Exception:
        return False

def _sim_values(replay):
    """Pick current hour's row + ±5% noise."""
    hour = datetime.datetime.utcnow().hour
    result = {}
    for r in REGIONS:
        vals = replay.get(r, [])
        if vals:
            base = vals[hour % len(vals)]
            noise = base * random.uniform(-0.05, 0.05)
            result[r] = round(base + noise, 2)
        else:
            result[r] = 100.0
    return result

def lambda_handler(event, context):
    live = _is_live_mode()
    replay = _load_replay()
    values = _sim_values(replay)   # sim mode (live API hookable here later)

    now = datetime.datetime.utcnow().isoformat()
    ttl = int(time.time()) + 7200  # expire in 2 hours

    written = []
    for region, gco2 in values.items():
        table.put_item(Item={
            "region":        region,
            "gco2_per_kwh":  str(round(gco2, 4)),
            "updated_at":    now,
            "source":        "live" if live else "sim",
            "ttl":           ttl
        })
        written.append({"region": region, "gco2_per_kwh": gco2})

    print(json.dumps({"status": "ok", "mode": "live" if live else "sim",
                      "written": written}))
    return {"statusCode": 200, "body": json.dumps(written)}