import os
import sys

# add project root to the system path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print(" Benchmark: Access Control Accuracy Based on Role & Trust")

# simulated policy map from your IAM app route
ACCESS_POLICIES = {
    'finance':   {'role': 'admin', 'min_trust': 0.8},
    'hr':        {'role': 'user',  'min_trust': 0.6},
    'devops':    {'role': 'admin', 'min_trust': 0.7},
    'projects':  {'role': 'user',  'min_trust': 0.5},
    'research':  {'role': 'guest', 'min_trust': 0.4}
}

# test data simulating users trying to access apps
test_cases = [
    {'app': 'finance',  'role': 'admin', 'trust': 0.85},  
    {'app': 'devops',   'role': 'admin', 'trust': 0.65},  
    {'app': 'hr',       'role': 'user',  'trust': 0.55},  
    {'app': 'projects', 'role': 'user',  'trust': 0.45},  
    {'app': 'research', 'role': 'guest', 'trust': 0.5},   
    {'app': 'research', 'role': 'user',  'trust': 0.3},  
    {'app': 'research', 'role': 'guest', 'trust': 0.2},  
    {'app': 'hr',       'role': 'admin', 'trust': 0.9},   
]

def evaluate_access(app, role, trust_score):
    policy = ACCESS_POLICIES.get(app)
    if not policy:
        return False, f"[{app}] Unknown app."

    has_role = role == policy['role']
    trust_ok = trust_score >= policy['min_trust']
    decision = has_role and trust_ok

    decision_str = "✅ ALLOWED" if decision else "❌ DENIED"
    explanation = f"[{app}] {decision_str} (Role={role}, Trust={trust_score}, Required: {policy})"
    return decision, explanation

# run test cases
results = []
for case in test_cases:
    allowed, message = evaluate_access(case['app'], case['role'], case['trust'])
    print(message)
    results.append(allowed)

# compute accuracy
accuracy = (results.count(True) / len(results)) * 100
print(f"\n🎯 Final Access Control Accuracy: {round(accuracy, 2)}% ({results.count(True)}/{len(results)})")
