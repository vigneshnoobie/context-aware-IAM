import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
import joblib

# load data
data = pd.read_csv('backend/ml/training_data.csv')

# features and Labels
X = data[['typing_speed', 'ip_risk', 'time_risk', 'device_change', 'location_distance']]
y = data['label']

# train-test split (optional)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# save model
joblib.dump(model, 'backend/ml/risk_model.pkl')
print("[✅] Model trained and saved as risk_model.pkl")

# after training the model
y_pred = model.predict(X)
accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred)

print(f"[📊] Accuracy: {accuracy:.2f}")
print(f"[📊] Precision: {precision:.2f}")
