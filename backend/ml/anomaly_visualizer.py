# backend/ml/anomaly_visualizer.py

import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def get_risk_heatmap(user_id):
    data = np.random.rand(10, 10)
    fig, ax = plt.subplots()
    cax = ax.imshow(data, cmap='hot')
    plt.title(f"Risk Heatmap - {user_id}")
    plt.colorbar(cax)
    return _fig_to_base64(fig)

def get_behavior_deviation_chart(user_id):
    x = list(range(1, 11))
    y = [np.random.rand() for _ in x]
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    plt.title(f"Behavior Deviation - {user_id}")
    plt.xlabel("Session")
    plt.ylabel("Deviation")
    return _fig_to_base64(fig)

def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded
