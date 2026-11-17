from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx
import boto3
import json
import os
from datetime import datetime, timezone
from mangum import Mangum

app = FastAPI(
    title="Carbon-Aware Serverless Scheduler API",
    description="""
    A production-grade REST API for scheduling serverless functions 
    across AWS regions based on real-time carbon intensity data.
    
    Routes workloads to the greenest available region using policies:
    - **carbon-only**: lowest carbon intensity wins
    - **multi-objective**: weighted score of carbon + latency + cost
    - **round-robin**: even distribution across regions
    - **always-home**: always route to home region (baseline)
    """,
    version="1.0.0",
    contact={
        "name": "Gayatri Mishra",
        "url": "https://github.com/gayatrimishraa/carbon-scheduler"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Config ---
ROUTER_FUNCTION_URL = os.environ.get("ROUTER_FUNCTION_URL", "")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "carbon-intensity-data")
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

# --- Models ---
class ScheduleRequest(BaseModel):
    payload: dict
    policy: str = "carbon-only"
    priority: Optional[str] = "normal"  # normal | high
    deadline_minutes: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "payload": {"task": "process-batch", "items": 100},
                "policy": "carbon-only",
                "priority": "normal",
                "deadline_minutes": 60
            }
        }

class ScheduleResponse(BaseModel):
    request_id: str
    selected_region: str
    policy_used: str
    carbon_intensity: float
    estimated_savings_gco2: float
    execution_time_ms: float
    timestamp: str

class CarbonIntensityResponse(BaseModel):
    region: str
    zone: str
    carbon_intensity_gco2_per_kwh: float
    forecast_next_hour: Optional[float]
    timestamp: str
    source: str

class PolicyComparisonResponse(BaseModel):
    policies: List[dict]
    recommended: str
    total_carbon_saved_gco2: float

# --- Endpoints ---

@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Carbon-Aware Serverless Scheduler",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.post("/schedule", response_model=ScheduleResponse, tags=["Scheduling"])
async def schedule_function(request: ScheduleRequest):
    """
    Schedule a serverless function execution using the specified carbon-aware policy.
    
    The router Lambda selects the optimal AWS region based on current carbon 
    intensity data stored in DynamoDB, then dispatches the payload to a 
    worker Lambda in that region.
    
    **Policies:**
    - `carbon-only` — minimise gCO2/kWh, ignore latency
    - `multi-objective` — weighted score: 50% carbon, 30% latency, 20% cost
    - `round-robin` — distribute load evenly, ignore carbon
    - `always-home` — always use ap-south-1 (baseline for comparison)
    """
    if not ROUTER_FUNCTION_URL:
        raise HTTPException(status_code=503, detail="Router Lambda URL not configured")
    
    start = datetime.now(timezone.utc)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                ROUTER_FUNCTION_URL,
                json={
                    "payload": request.payload,
                    "policy": request.policy,
                    "priority": request.priority,
                    "deadline_minutes": request.deadline_minutes
                }
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Router Lambda timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Router error: {str(e)}")
    
    elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
    
    return ScheduleResponse(
        request_id=data.get("request_id", f"req-{int(start.timestamp())}"),
        selected_region=data.get("selected_region", "unknown"),
        policy_used=request.policy,
        carbon_intensity=data.get("carbon_intensity", 0.0),
        estimated_savings_gco2=data.get("estimated_savings_gco2", 0.0),
        execution_time_ms=round(elapsed, 2),
        timestamp=start.isoformat()
    )

@app.get("/carbon-intensity", tags=["Carbon Data"])
async def get_carbon_intensity(
    regions: Optional[str] = Query(None, description="Comma-separated region codes, e.g. us-east-1,eu-north-1")
):
    """
    Get current carbon intensity across all monitored AWS regions.
    Data is sourced from DynamoDB (populated by the collector Lambda).
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.scan()
        items = response.get("Items", [])
        
        if regions:
            filter_regions = [r.strip() for r in regions.split(",")]
            items = [i for i in items if i.get("region") in filter_regions]
        
        # Sort by carbon intensity ascending (greenest first)
        items.sort(key=lambda x: float(x.get("carbon_intensity", 999)))
        
        return {
            "regions": items,
            "greenest_region": items[0].get("region") if items else None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/carbon-intensity/{region}", tags=["Carbon Data"])
async def get_region_carbon_intensity(region: str):
    """
    Get carbon intensity for a specific AWS region.
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.get_item(Key={"region": region})
        item = response.get("Item")
        if not item:
            raise HTTPException(status_code=404, detail=f"Region {region} not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/execution-history", tags=["Analytics"])
async def get_execution_history(
    limit: int = Query(20, ge=1, le=100),
    policy: Optional[str] = Query(None, description="Filter by policy name")
):
    """
    Retrieve past scheduling decisions with carbon savings data.
    Useful for auditing and policy comparison dashboards.
    """
    try:
        table = dynamodb.Table("carbon-execution-log")
        if policy:
            response = table.scan(
                FilterExpression="policy_used = :p",
                ExpressionAttributeValues={":p": policy}
            )
        else:
            response = table.scan()
        
        items = response.get("Items", [])
        items.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return {"executions": items[:limit], "count": len(items[:limit])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/policies/compare", tags=["Analytics"])
async def compare_policies():
    """
    Compare carbon efficiency across all scheduling policies using 
    historical execution data from DynamoDB.
    """
    try:
        table = dynamodb.Table("carbon-execution-log")
        response = table.scan()
        items = response.get("Items", [])
        
        policy_stats = {}
        for item in items:
            p = item.get("policy_used", "unknown")
            if p not in policy_stats:
                policy_stats[p] = {"count": 0, "total_carbon": 0.0, "total_savings": 0.0}
            policy_stats[p]["count"] += 1
            policy_stats[p]["total_carbon"] += float(item.get("carbon_intensity", 0))
            policy_stats[p]["total_savings"] += float(item.get("estimated_savings_gco2", 0))
        
        results = []
        for policy, stats in policy_stats.items():
            avg_carbon = stats["total_carbon"] / stats["count"] if stats["count"] else 0
            results.append({
                "policy": policy,
                "executions": stats["count"],
                "avg_carbon_intensity": round(avg_carbon, 2),
                "total_carbon_saved_gco2": round(stats["total_savings"], 4)
            })
        
        results.sort(key=lambda x: x["avg_carbon_intensity"])
        recommended = results[0]["policy"] if results else "carbon-only"
        
        return {
            "policies": results,
            "recommended": recommended,
            "note": "Lower avg_carbon_intensity = greener policy"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/regions", tags=["Infrastructure"])
def list_regions():
    """List all monitored AWS regions and their metadata."""
    return {
        "regions": [
            {"region": "us-east-1", "zone": "US-NY", "label": "N. Virginia"},
            {"region": "eu-north-1", "zone": "SE", "label": "Stockholm"},
            {"region": "ap-south-1", "zone": "IN-MH", "label": "Mumbai (home)"},
        ],
        "home_region": "ap-south-1"
    }

# Mangum handler for Lambda deployment
handler = Mangum(app)