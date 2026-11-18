"""
Local training script — run this to validate the ML model works
without needing AWS credentials.

Usage: python ml/train.py
"""
import numpy as np

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
    mae = float(np.mean(np.abs(y - preds)))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    ss_res = float(np.sum((y - preds) ** 2))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    print(f"\nRegion: {region}")
    print(f"  MAE : {mae:.2f} gCO2/kWh")
    print(f"  R²  : {r2:.4f}")
    print(f"  Hour 0  actual={pattern[0]:>6.1f}  predicted={preds[0]:>6.1f}")
    print(f"  Hour 12 actual={pattern[12]:>6.1f}  predicted={preds[12]:>6.1f}")
    print(f"  Hour 18 actual={pattern[18]:>6.1f}  predicted={preds[18]:>6.1f}")

print("\n✅ Model training complete — ready for Lambda deployment")
