import json
import boto3
import numpy as np
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal

# Pure NumPy implementations of StandardScaler and Ridge regression
# Eliminates heavy scikit-learn and scipy dependencies for lightweight, reliable Lambda deployment
class StandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        self.mean_ = np.mean(X, axis=0)
        self.scale_ = np.std(X, axis=0)
        self.scale_[self.scale_ == 0.0] = 1.0
        return (X - self.mean_) / self.scale_

    def transform(self, X: np.ndarray) -> np.ndarray:
        return (X - self.mean_) / self.scale_


class Ridge:
    def __init__(self, alpha: float = 1.0):
        self.alpha = float(alpha)
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.intercept_ = float(np.mean(y))
        y_centered = y - self.intercept_
        n_features = X.shape[1]
        A = X.T @ X + self.alpha * np.eye(n_features)
        b = X.T @ y_centered
        self.coef_ = np.linalg.solve(A, b)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return (X @ self.coef_) + self.intercept_


CARBON_TABLE = os.environ.get("CARBON_TABLE", "carbon_live")
FORECAST_TABLE = os.environ.get("FORECAST_TABLE", "region_state")
DYNAMODB_REGION = os.environ.get("DYNAMODB_REGION", "ap-south-1")

dynamodb = boto3.resource("dynamodb", region_name=DYNAMODB_REGION)

REGIONS = ["ap-south-1", "eu-north-1", "us-east-1"]

# Simulated historical pattern per region (gCO2/kWh by hour of day)
# Based on real-world grid patterns: renewables peak midday, fossil peaks evening
REGION_PATTERNS = {
    "ap-south-1": [210,205,200,195,190,185,175,160,145,130,120,115,
                   118,125,135,148,162,178,192,200,208,212,215,212],
    "eu-north-1": [ 28, 26, 24, 23, 22, 21, 20, 18, 17, 16, 15, 14,
                    15, 16, 18, 20, 22, 25, 28, 30, 31, 30, 29, 28],
    "us-east-1":  [320,310,300,295,290,285,280,275,270,265,260,258,
                   260,268,278,290,305,318,328,335,338,335,330,325],
}

def build_features(hour: int, region: str) -> np.ndarray:
    """
    Feature vector for a given hour:
    - hour of day (0-23)
    - sin/cos encoding of hour (captures cyclical pattern)
    - is_peak_hour (1 if 17-21, else 0)
    - is_renewable_peak (1 if 10-15, else 0)
    - region baseline (avg gCO2/kWh for region)
    """
    baseline = np.mean(REGION_PATTERNS.get(region, [200]*24))
    return np.array([
        hour,
        np.sin(2 * np.pi * hour / 24),
        np.cos(2 * np.pi * hour / 24),
        1 if 17 <= hour <= 21 else 0,
        1 if 10 <= hour <= 15 else 0,
        baseline
    ])

def train_model(region: str):
    """
    Train a Ridge regression model on the region's hourly carbon pattern.
    Returns fitted model and scaler.
    """
    pattern = REGION_PATTERNS.get(region, [200]*24)
    
    X = np.array([build_features(h, region) for h in range(24)])
    y = np.array(pattern, dtype=float)
    
    # Add small gaussian noise to simulate real variance
    np.random.seed(42)
    y_noisy = y + np.random.normal(0, 3, size=y.shape)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = Ridge(alpha=1.0)
    model.fit(X_scaled, y_noisy)
    
    return model, scaler

def get_current_intensity(region: str) -> float:
    """Read current carbon intensity from DynamoDB carbon_live table."""
    try:
        table = dynamodb.Table(CARBON_TABLE)
        response = table.get_item(Key={"region": region})
        item = response.get("Item")
        if item:
            return float(item.get("gco2_per_kwh", 200))
    except Exception as e:
        print(f"DynamoDB read error for {region}: {e}")
    return 200.0

def write_forecast(region: str, current: float, forecast: float,
                   trend: str, confidence: float):
    """Write forecast back to region_state table."""
    try:
        table = dynamodb.Table(FORECAST_TABLE)
        table.update_item(
            Key={"region": region},
            UpdateExpression="""
                SET forecast_next_hour = :f,
                    current_intensity = :c,
                    forecast_trend = :t,
                    forecast_confidence = :conf,
                    forecast_updated_at = :ts,
                    forecast_model = :m
            """,
            ExpressionAttributeValues={
                ":f": Decimal(str(round(forecast, 2))),
                ":c": Decimal(str(round(current, 2))),
                ":t": trend,
                ":conf": Decimal(str(round(confidence, 3))),
                ":ts": datetime.now(timezone.utc).isoformat(),
                ":m": "ridge-regression-v1"
            }
        )
        print(f"[{region}] forecast written: current={current:.1f} "
              f"next={forecast:.1f} trend={trend}")
    except Exception as e:
        print(f"DynamoDB write error for {region}: {e}")

def lambda_handler(event, context):
    """
    Main Lambda handler.
    - Reads current carbon intensity per region from DynamoDB
    - Trains Ridge regression model per region
    - Predicts next-hour carbon intensity
    - Writes forecast back to region_state table
    """
    now = datetime.now(timezone.utc)
    next_hour = (now + timedelta(hours=1)).hour
    
    results = []

    for region in REGIONS:
        try:
            # Get current reading
            current = get_current_intensity(region)
            
            # Train model and predict next hour
            model, scaler = train_model(region)
            features = build_features(next_hour, region).reshape(1, -1)
            features_scaled = scaler.transform(features)
            forecast = float(model.predict(features_scaled)[0])
            forecast = max(10.0, forecast)  # floor at 10 gCO2/kWh
            
            # Determine trend
            diff = forecast - current
            if diff > 5:
                trend = "increasing"
            elif diff < -5:
                trend = "decreasing"
            else:
                trend = "stable"
            
            # Confidence: inverse of prediction uncertainty (simplified)
            pattern = REGION_PATTERNS.get(region, [200]*24)
            std = float(np.std(pattern))
            confidence = round(1.0 / (1.0 + abs(diff) / (std + 1e-6)), 3)
            
            write_forecast(region, current, forecast, trend, confidence)
            
            results.append({
                "region": region,
                "current_gco2_kwh": round(current, 2),
                "forecast_next_hour_gco2_kwh": round(forecast, 2),
                "trend": trend,
                "confidence": confidence
            })

        except Exception as e:
            print(f"Error processing {region}: {e}")
            results.append({"region": region, "error": str(e)})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "timestamp": now.isoformat(),
            "forecasts": results,
            "model": "ridge-regression-v1",
            "next_hour": next_hour
        })
    }


# Local test
if __name__ == "__main__":
    result = lambda_handler({}, None)
    print(json.dumps(json.loads(result["body"]), indent=2))
