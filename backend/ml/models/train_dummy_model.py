# backend/ml/train_model.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Dummy data for training
X = np.random.rand(100, 4)  # 100 samples, 4 features
y = np.random.randint(0, 2, 100)  # binary labels

# Train a simple model
model = RandomForestClassifier()
model.fit(X, y)

# Save it using joblib in the current environment
joblib.dump(model, 'backend/ml/risk_model.pkl')

print("[✅] Model trained and saved successfully.")
