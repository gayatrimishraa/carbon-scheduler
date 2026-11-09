import csv, json, pathlib
import matplotlib
matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

DATA_DIR   = pathlib.Path(__file__).parent.parent / "data"
CHARTS_DIR = pathlib.Path(__file__).parent.parent / "data" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_JSON = DATA_DIR / "summary.json"
RAW_CSV      = DATA_DIR / "results_raw.csv"

POLICIES     = ["home", "round_robin", "carbon_only", "multi_objective"]
COLORS       = {"home":"#4C72B0", "round_robin":"#DD8452",
                "carbon_only":"#55A868", "multi_objective":"#C44E52"}
LABELS       = {"home":"Home", "round_robin":"Round Robin",
                "carbon_only":"Carbon Only", "multi_objective":"Multi-Objective"}

def load_summary():
    with open(SUMMARY_JSON) as f:
        return json.load(f)

FIELDNAMES = ["run_id","repeat","policy","sim_hour","request_id","chosen_region",
              "latency_ms","wall_ms","cold_start","est_gco2","carbon_intensity",
              "score_ap","score_eu","score_us","error","timestamp"]

def load_raw():
    rows = []
    with open(RAW_CSV, newline="") as f:
        for r in csv.DictReader(f, fieldnames=FIELDNAMES):
            rows.append(r)
    return rows

# ── Chart 1: Total estimated CO2 per policy ──────────────────────────────────
def chart_total_co2(summary):
    fig, ax = plt.subplots(figsize=(8, 5))
    policies = [p for p in POLICIES if p in summary]
    vals     = [summary[p]["total_gco2"] for p in policies]
    bars     = ax.bar([LABELS[p] for p in policies], vals,
                      color=[COLORS[p] for p in policies], width=0.5)
    ax.bar_label(bars, fmt="%.4f", padding=3, fontsize=9)
    ax.set_title("Total Estimated CO₂ Emissions by Policy (gCO₂)", fontsize=13)
    ax.set_ylabel("Total gCO₂")
    ax.set_xlabel("Scheduling Policy")
    plt.tight_layout()
    out = CHARTS_DIR / "chart1_total_co2.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")

# ── Chart 2: Average latency + P95 latency ───────────────────────────────────
def chart_latency(summary):
    fig, ax = plt.subplots(figsize=(8, 5))
    policies = [p for p in POLICIES if p in summary]
    x        = np.arange(len(policies))
    avg_lat  = [summary[p]["avg_latency_ms"] for p in policies]
    p95_lat  = [summary[p]["p95_latency_ms"] for p in policies]
    w = 0.35
    b1 = ax.bar(x - w/2, avg_lat, w, label="Avg Latency",
                color=[COLORS[p] for p in policies], alpha=0.85)
    b2 = ax.bar(x + w/2, p95_lat, w, label="P95 Latency",
                color=[COLORS[p] for p in policies], alpha=0.45,
                edgecolor="black", linewidth=0.6)
    ax.bar_label(b1, fmt="%.0f", padding=2, fontsize=8)
    ax.bar_label(b2, fmt="%.0f", padding=2, fontsize=8)
    ax.set_title("Latency by Policy (ms)", fontsize=13)
    ax.set_ylabel("Latency (ms)")
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[p] for p in policies])
    ax.legend()
    plt.tight_layout()
    out = CHARTS_DIR / "chart2_latency.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")

# ── Chart 3: Cold start rate ──────────────────────────────────────────────────
def chart_cold_starts(summary):
    fig, ax = plt.subplots(figsize=(8, 5))
    policies = [p for p in POLICIES if p in summary]
    rates    = [summary[p]["cold_start_rate"] * 100 for p in policies]
    bars     = ax.bar([LABELS[p] for p in policies], rates,
                      color=[COLORS[p] for p in policies], width=0.5)
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=9)
    ax.set_title("Cold Start Rate by Policy (%)", fontsize=13)
    ax.set_ylabel("Cold Start Rate (%)")
    ax.set_ylim(0, max(rates) * 1.3 + 1)
    plt.tight_layout()
    out = CHARTS_DIR / "chart3_cold_starts.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")

# ── Chart 4: Region distribution (stacked bar) ───────────────────────────────
def chart_region_dist(summary):
    regions  = ["ap-south-1", "eu-north-1", "us-east-1"]
    reg_colors = ["#4C72B0", "#55A868", "#DD8452"]
    policies = [p for p in POLICIES if p in summary]
    fig, ax  = plt.subplots(figsize=(8, 5))
    bottoms  = np.zeros(len(policies))
    for reg, col in zip(regions, reg_colors):
        vals = [summary[p]["region_distribution"].get(reg, 0) for p in policies]
        ax.bar([LABELS[p] for p in policies], vals, bottom=bottoms,
               label=reg, color=col, alpha=0.85, width=0.5)
        bottoms += np.array(vals)
    ax.set_title("Region Selection Distribution by Policy", fontsize=13)
    ax.set_ylabel("Number of Requests")
    ax.legend(title="Region")
    plt.tight_layout()
    out = CHARTS_DIR / "chart4_region_dist.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")

# ── Chart 5: CO2 over time (rolling avg per policy) ──────────────────────────
def chart_co2_over_time(rows):
    from collections import defaultdict
    policy_rows = defaultdict(list)
    for r in rows:
        policy_rows[r["policy"]].append(float(r["est_gco2"]))

    fig, ax = plt.subplots(figsize=(10, 5))
    for policy in POLICIES:
        vals = policy_rows.get(policy, [])
        if not vals:
            continue
        window = 20
        rolling = [np.mean(vals[max(0,i-window):i+1]) for i in range(len(vals))]
        ax.plot(rolling, label=LABELS[policy], color=COLORS[policy], linewidth=1.5)
    ax.set_title("Rolling Avg CO₂ per Request Over Time (window=20)", fontsize=13)
    ax.set_xlabel("Request index")
    ax.set_ylabel("Est. gCO₂")
    ax.legend()
    plt.tight_layout()
    out = CHARTS_DIR / "chart5_co2_over_time.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")

if __name__ == "__main__":
    summary = load_summary()
    rows    = load_raw()
    chart_total_co2(summary)
    chart_latency(summary)
    chart_cold_starts(summary)
    chart_region_dist(summary)
    chart_co2_over_time(rows)
    print(f"\nAll charts saved to {CHARTS_DIR}")