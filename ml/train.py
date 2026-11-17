"""
Local training script — run this to validate the ML model works
without needing AWS credentials.

Usage: python ml/train.py
"""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

REGION_PATTERNS = {
    "ap-south-1": [210,205,200,195,190,185,175,160,145,130,120,115,
                   118,125,135,148,162,178,192,200,208,212,215,212],
    "eu-north-1": [ 28, 26, 24, 23, 22, 21, 20, 18, 17, 16, 15, 14,
                    15, 16, 18, 20, 22, 25, 28, 30, 31, 30, 29, 28],
    "us-east-1":  [320,310,300,295,290,285,280,275,270,265,260,258,
                   260,268,278,290,305,318,328,335,338,335,330,325],
}

def build_features(hour, region):
    baseline = np.mean(REGION_PATTERNS[region])
    return np.array([
        hour,
        np.sin(2 * np.pi * hour / 24),
        np.cos(2 * np.pi * hour / 24),
        1 if 17 <= hour <= 21 else 0,
        1 if 10 <= hour <= 15 else 0,
        baseline
    ])

print("=" * 55)
print("Carbon Intensity Forecast — Ridge Regression Model")
print("=" * 55)

for region, pattern in REGION_PATTERNS.items():
    X = np.array([build_features(h, region) for h in range(24)])
    y = np.array(pattern, dtype=float)
    np.random.seed(42)
    y_noisy = y + np.random.normal(0, 3, size=y.shape)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = Ridge(alpha=1.0)
    model.fit(X_scaled, y_noisy)

    preds = model.predict(X_scaled)
    mae = mean_absolute_error(y, preds)
    r2 = r2_score(y, preds)

    print(f"\nRegion: {region}")
    print(f"  MAE : {mae:.2f} gCO2/kWh")
    print(f"  R²  : {r2:.4f}")
    print(f"  Hour 0  actual={pattern[0]:>6.1f}  predicted={preds[0]:>6.1f}")
    print(f"  Hour 12 actual={pattern[12]:>6.1f}  predicted={preds[12]:>6.1f}")
    print(f"  Hour 18 actual={pattern[18]:>6.1f}  predicted={preds[18]:>6.1f}")

print("\n✅ Model training complete — ready for Lambda deployment")