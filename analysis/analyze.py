import csv, json, pathlib, statistics
from collections import defaultdict

RAW_CSV  = pathlib.Path(__file__).parent.parent / "data" / "results_raw.csv"
OUT_JSON = pathlib.Path(__file__).parent.parent / "data" / "summary.json"
OUT_CSV  = pathlib.Path(__file__).parent.parent / "data" / "summary.csv"

FIELDNAMES = ["run_id","repeat","policy","sim_hour","request_id","chosen_region",
              "latency_ms","wall_ms","cold_start","est_gco2","carbon_intensity",
              "score_ap","score_eu","score_us","error","timestamp"]

def load_raw():
    rows = []
    with open(RAW_CSV, newline="") as f:
        for r in csv.DictReader(f, fieldnames=FIELDNAMES):
            rows.append(r)
    print(f"Loaded {len(rows)} rows from {RAW_CSV}")
    return rows

def safe_float(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default

def analyze(rows):
    by_policy = defaultdict(list)
    for r in rows:
        if r.get("error"):
            continue
        by_policy[r["policy"]].append(r)

    summary = {}
    for policy, prows in by_policy.items():
        gco2_vals    = [safe_float(r["est_gco2"])   for r in prows]
        latency_vals = [safe_float(r["latency_ms"]) for r in prows]
        cold_vals    = [1 if str(r["cold_start"]).lower()=="true" else 0
                        for r in prows]
        region_counts = defaultdict(int)
        for r in prows:
            region_counts[r["chosen_region"]] += 1

        summary[policy] = {
            "n":                   len(prows),
            "avg_gco2":            round(statistics.mean(gco2_vals), 6),
            "total_gco2":          round(sum(gco2_vals), 4),
            "avg_latency_ms":      round(statistics.mean(latency_vals), 2),
            "p95_latency_ms":      round(sorted(latency_vals)[int(len(latency_vals)*0.95)], 2),
            "cold_start_rate":     round(sum(cold_vals)/len(cold_vals), 4),
            "cold_start_count":    sum(cold_vals),
            "region_distribution": dict(region_counts),
        }
    return summary

def print_table(summary):
    print(f"\n{'Policy':<20} {'N':>5} {'Avg gCO2':>12} {'Total gCO2':>12} "
          f"{'Avg Lat ms':>12} {'P95 Lat ms':>12} {'Cold%':>8}")
    print("-"*85)
    for policy, s in sorted(summary.items()):
        print(f"{policy:<20} {s['n']:>5} {s['avg_gco2']:>12.6f} "
              f"{s['total_gco2']:>12.4f} {s['avg_latency_ms']:>12.2f} "
              f"{s['p95_latency_ms']:>12.2f} {s['cold_start_rate']*100:>7.1f}%")

def save_outputs(summary):
    with open(OUT_JSON, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved {OUT_JSON}")
    fields = ["policy","n","avg_gco2","total_gco2","avg_latency_ms",
              "p95_latency_ms","cold_start_rate","cold_start_count"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for policy, s in sorted(summary.items()):
            w.writerow({"policy": policy, **s})
    print(f"Saved {OUT_CSV}")

if __name__ == "__main__":
    rows    = load_raw()
    summary = analyze(rows)
    print_table(summary)
    save_outputs(summary)
    print("\nDone.")