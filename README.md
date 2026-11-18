# 🌱 Carbon-Aware Serverless Function Scheduler

A production-grade, cloud-native system that routes AWS Lambda
workloads to the **greenest available region** in real time —
minimising carbon emissions from serverless compute.

Built with Python, AWS SAM, FastAPI, and a custom ML forecasting
pipeline. Deployed across 3 AWS regions with full CI/CD.

---

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │   FastAPI REST   │
                    │   (api/app.py)   │
                    └────────┬────────┘
                             │ POST /schedule
                    ┌────────▼────────┐
                    │  carbon-router  │◄── Function URL
                    │    (Lambda)     │
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
   ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
   │ carbon-worker │ │ carbon-worker │ │ carbon-worker │
   │  ap-south-1   │ │  eu-north-1   │ │  us-east-1    │
   │   (Mumbai)    │ │  (Stockholm)  │ │  (N.Virginia) │
   └───────────────┘ └───────────────┘ └───────────────┘

           ┌─────────────────────────────────┐
           │         DynamoDB (ap-south-1)    │
           │  carbon_live │ region_state      │
           │              │ requests          │
           └─────────────────────────────────┘
                             ▲
              ┌──────────────┴──────────────┐
              │                             │
   ┌──────────────────┐         ┌───────────────────┐
   │ carbon-collector │         │ carbon-ml-forecast │
   │ (hourly via EB)  │         │ (hourly via EB)    │
   │ writes carbon    │         │ Ridge regression   │
   │ intensity data   │         │ next-hour forecast │
   └──────────────────┘         └───────────────────┘
```

---

## 🚀 Scheduling Policies

| Policy | Logic | Use Case |
|---|---|---|
| `carbon-only` | Lowest gCO2/kWh wins | Maximum green impact |
| `multi-objective` | 50% carbon + 30% latency + 20% cost | Balanced production |
| `round-robin` | Even distribution | Baseline comparison |
| `always-home` | Always ap-south-1 | Latency-critical |

---

## 🤖 ML Forecasting

The `carbon-ml-forecast` Lambda runs **hourly via EventBridge**
and predicts next-hour carbon intensity for each region using
a **Ridge regression model** built with pure NumPy (no scipy —
stays within Lambda's 250MB limit).

Features used: hour of day, day of week, rolling mean,
rolling std, lag-1, lag-24.

Forecasts are written to the `region_state` DynamoDB table
and used by the router for proactive scheduling decisions.

---

## 🌐 REST API

Base URL: deployed via FastAPI + Mangum (Lambda-compatible)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service info + health |
| GET | `/health` | Health check |
| POST | `/schedule` | Schedule a function execution |
| GET | `/carbon-intensity` | All regions, sorted greenest first |
| GET | `/carbon-intensity/{region}` | Single region carbon data |
| GET | `/execution-history` | Past scheduling decisions |
| GET | `/policies/compare` | Carbon savings by policy |
| GET | `/regions` | All monitored regions |

Interactive docs available at `/docs` (Swagger UI) when
running locally.

---

## ⚙️ Infrastructure

- **IaC:** AWS SAM (`template.yaml`) — single unified stack
- **Stack name:** `carbon-aware-scheduler`
- **Home region:** `ap-south-1` (Mumbai)
- **Worker regions:** `ap-south-1`, `eu-north-1`, `us-east-1`
- **Budget:** $0 (AWS Free Tier only)
- **No VPC, no RDS, no EC2**

---

## 🔄 CI/CD

GitHub Actions workflow (`.github/workflows/deploy.yml`)
triggers on every push to `main`:

```
push to main → sam build → sam deploy → CloudFormation UPDATE_COMPLETE
```

---

## 📊 Monitoring

CloudWatch Dashboard: **CarbonAwareScheduler**
- Router invocations, errors, p99 duration
- Worker invocations by region
- ML forecast Lambda health
- Cold starts across all functions
- Concurrent executions

---

## 🛠️ Local Setup

```bash
# Install dependencies
cd api && pip install -r requirements.txt

# Run FastAPI locally
uvicorn app:app --reload
# → http://localhost:8000/docs

# Build + deploy SAM stack
sam build --region ap-south-1
sam deploy --region ap-south-1 \
  --stack-name carbon-aware-scheduler \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
  --no-confirm-changeset
```

---

## 📁 Project Structure

```
carbon-scheduler/
├── collector/        # Lambda: hourly carbon data collector
├── router/           # Lambda: policy-based region selector  
├── worker/           # Lambda: workload executor (3 regions)
├── ml/               # Lambda: Ridge regression forecaster
├── api/              # FastAPI REST layer
├── analysis/         # Policy comparison scripts
├── data/             # Historical carbon replay data
├── loadgen/          # Load generator
├── scripts/          # Utility scripts
├── template.yaml     # SAM unified stack
├── index.html        # Local dashboard
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## 🌍 Why This Matters

Carbon-aware computing is an emerging discipline in sustainable 
software engineering. Every serverless function execution consumes 
energy — and the carbon intensity of that energy varies dramatically 
by region and time of day. Stockholm's grid runs on ~20 gCO2/kWh 
during off-peak hours; Virginia can hit ~400 gCO2/kWh during peak 
demand. This system makes those differences actionable at the 
infrastructure level, automatically routing compute to where the 
grid is cleanest — reducing the carbon footprint of every execution 
without any change to application code.