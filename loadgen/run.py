import csv, json, time, random, pathlib, datetime, os
import urllib.request, urllib.error

# ── config ────────────────────────────────────────────────────────────────────
URL     = "https://r5ayxprhq2kwb6i6wdbar4o7m40fqrca.lambda-url.ap-south-1.on.aws/"
TOKEN   = "scheduler-secret-2024"
POLICIES = ["home", "round_robin", "carbon_only", "multi_objective"]
REPEATS  = 3
COLD_START_SLEEP = 370   # 6m10s → forces cold start (Lambda idle timeout ~5min)
OUT_CSV  = pathlib.Path(__file__).parent.parent / "data" / "results_raw.csv"

# ── load replay trace ─────────────────────────────────────────────────────────
TRACE_CSV = pathlib.Path(__file__).parent.parent / "data" / "carbon_replay.csv"
trace = []
with open(TRACE_CSV, newline="") as f:
    for row in csv.DictReader(f):
        trace.append(int(row["hour_index"]))   # adjust column name if different

# use first 300 rows (or all if fewer)
trace = trace[:300]
print(f"Loaded {len(trace)} trace rows")

# ── helpers ───────────────────────────────────────────────────────────────────
def invoke(policy, sim_hour, run_id):
    payload = json.dumps({"policy": policy, "sim_hour": sim_hour,
                          "run_id": run_id}).encode()
    req = urllib.request.Request(
        URL,
        data=payload,
        headers={"X-Scheduler-Token": TOKEN, "Content-Type": "application/json"},
        method="POST"
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
            body["wall_ms"] = round((time.time() - t0) * 1000, 1)
            body["error"]   = ""
            return body
    except Exception as e:
        return {"policy": policy, "sim_hour": sim_hour, "run_id": run_id,
                "error": str(e), "wall_ms": round((time.time() - t0)*1000, 1)}

# ── main loop ─────────────────────────────────────────────────────────────────
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
fieldnames = ["run_id","repeat","policy","sim_hour","request_id","chosen_region",
              "latency_ms","wall_ms","cold_start","est_gco2","carbon_intensity",
              "score_ap","score_eu","score_us","error","timestamp"]

with open(OUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for repeat in range(1, REPEATS + 1):
        for policy in POLICIES:
            run_id = f"{policy}_r{repeat}"
            print(f"\n{'='*55}")
            print(f"  Policy={policy}  Repeat={repeat}/{REPEATS}  ({len(trace)} reqs)")
            print(f"  Sleeping {COLD_START_SLEEP}s to force cold start…")
            time.sleep(COLD_START_SLEEP)

            ok = err = 0
            for i, sim_hour in enumerate(trace):
                result = invoke(policy, sim_hour, run_id)
                scores = result.get("scores", {})
                row = {
                    "run_id":           run_id,
                    "repeat":           repeat,
                    "policy":           policy,
                    "sim_hour":         sim_hour,
                    "request_id":       result.get("request_id",""),
                    "chosen_region":    result.get("chosen_region",""),
                    "latency_ms":       result.get("latency_ms",""),
                    "wall_ms":          result.get("wall_ms",""),
                    "cold_start":       result.get("cold_start",""),
                    "est_gco2":         result.get("est_gco2",""),
                    "carbon_intensity": result.get("carbon_intensity",""),
                    "score_ap":         scores.get("ap-south-1",""),
                    "score_eu":         scores.get("eu-north-1",""),
                    "score_us":         scores.get("us-east-1",""),
                    "error":            result.get("error",""),
                    "timestamp":        datetime.datetime.utcnow().isoformat(),
                }
                with open(OUT_CSV, "a", newline="") as f2:
                    csv.DictWriter(f2, fieldnames=fieldnames,
                                   extrasaction="ignore").writerow(row)
                if result.get("error"):
                    err += 1
                    print(f"  [{i+1:3d}] ERROR: {result['error'][:60]}")
                else:
                    ok += 1
                    if (i+1) % 50 == 0:
                        print(f"  [{i+1:3d}] ok  region={result.get('chosen_region','')}  "
                              f"gco2={result.get('est_gco2','')}  cold={result.get('cold_start','')}")
                # small throttle to stay within Lambda concurrency
                time.sleep(0.05)

            print(f"  Done: {ok} ok, {err} errors → {OUT_CSV}")

print("\nAll runs complete.")