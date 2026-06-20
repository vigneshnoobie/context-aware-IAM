# federated_train.py - Federated Learning for Privacy-Preserving Risk Training
'''
Trains ML risk models using federated learning to preserve privacy by keeping raw user data local.


'''

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import random
import copy

# Simulated local datasets (would be edge devices/users in real-world FL)
user_datasets = {
    'user1': {'X': [[0.2, 0.3], [0.1, 0.5], [0.4, 0.6]], 'y': [0, 0, 1]},
    'user2': {'X': [[0.6, 0.7], [0.5, 0.4], [0.7, 0.8]], 'y': [1, 1, 0]},
    'user3': {'X': [[0.3, 0.3], [0.2, 0.2], [0.3, 0.4]], 'y': [0, 0, 1]}
}

# Simulate a centralized model (in production this is coordinated by a server)
GLOBAL_MODEL = DecisionTreeClassifier()


def train_local_model(X, y):
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model


def average_models(models):
    # In real FL, model weights are averaged; here, we choose the best performing
    return random.choice(models)  # placeholder for real aggregation


def simulate_federated_training(rounds=5):
    global GLOBAL_MODEL
    for r in range(rounds):
        local_models = []
        print(f"\n[Round {r + 1}] Training local models...")
        for user, data in user_datasets.items():
            model = train_local_model(data['X'], data['y'])
            local_models.append(model)
            acc = accuracy_score(data['y'], model.predict(data['X']))
            print(f"- {user} model accuracy: {acc:.2f}")

        GLOBAL_MODEL = average_models(local_models)
        print("[Model Aggregation] Global model updated.")


def test_global_model():
    test_X = [[0.25, 0.35], [0.6, 0.7]]
    predictions = GLOBAL_MODEL.predict(test_X)
    print("[Global Model Predictions]", predictions)


# Example run for development
if __name__ == '__main__':
    simulate_federated_training(rounds=3)
    test_global_model()
