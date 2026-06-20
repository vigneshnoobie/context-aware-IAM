# backend/auth/utils/behavioral_model.py

def analyze_behavior(typing_data, stored_pattern):
    """
    Analyzes typing behavior patterns. If no existing pattern is found, it defaults to scoring based solely on context. 
    The returned score ranges from 0 to 100, with higher values indicating a better match.
    """

    try:
        # If no typing data at all, assume neutral
        if not typing_data:
            return 70.0

        typing_values = list(map(int, typing_data.split(',')))

        #  If no stored pattern (first login or passwordless), use avg typing speed
        if not stored_pattern:
            avg_duration = sum(typing_values) / len(typing_values) if typing_values else 0

            if avg_duration < 100:
                return 80.0  # Fast but acceptable
            elif avg_duration < 200:
                return 60.0  # Slower but okay
            else:
                return 45.0  # Possibly suspicious

        # Compare typing behavior with stored pattern
        stored_values = list(map(int, stored_pattern.split(',')))
        min_len = min(len(typing_values), len(stored_values))
        typing_values = typing_values[:min_len]
        stored_values = stored_values[:min_len]

        diffs = [abs(t - s) for t, s in zip(typing_values, stored_values)]
        avg_diff = sum(diffs) / len(diffs)
        score = max(0.0, 100 - avg_diff)

        return round(score, 2)

    except Exception as e:
        print(f"[Behavioral Analysis Error] {e}")
        return 70.0  # Fallback to safe score
