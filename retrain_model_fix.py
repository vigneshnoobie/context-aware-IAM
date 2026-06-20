# retrain_model_fix.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


X = np.random.rand(100, 4)
y = np.random.randint(0, 2, 100)


model = RandomForestClassifier()
model.fit(X, y)


model_path = os.path.join('backend', 'ml', 'risk_model.pkl')


joblib.dump(model, model_path)

print(f"[✅]  model trained and saved successfully at {model_path}")
