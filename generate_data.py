import pandas as pd
import random
import csv

# Create 50 synthetic IAM login records
def generate_synthetic_data(num_rows=50):
    data = []
    for _ in range(num_rows):
        row = {
            "typing_speed": round(random.uniform(0.1, 0.8), 2),
            "ip_risk": random.choice([0, 1]),
            "time_risk": random.choice([0, 1]),
            "device_change": random.choice([0, 1]),
            "location_distance": round(random.uniform(0, 1000), 2),
            "label": random.choice([0, 1])  # 0 = safe, 1 = risky
        }
        data.append(row)
    return data

# Generate and save to CSV
if __name__ == "__main__":
    data = generate_synthetic_data(50)
    df = pd.DataFrame(data)
    output_path = "training_data.csv"
    df.to_csv(output_path, index=False)
    print(f"[✅] Generated {len(df)} rows in '{output_path}'")
