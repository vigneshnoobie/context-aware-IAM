# backend/apps/routes.py

"""
Application Routes
-------------------
Manages the simulation of external applications integrated with the IAM system. Each route corresponds to a secured resource, 
enforcing access control based on risk, trust, and context-aware policies.
"""

from flask import Blueprint, request, render_template, session, redirect, url_for
from backend.auth.utils.context_engine import collect_context_data
from backend.ml.scoring import compute_risk_score
from backend.ml.atfe import update_trust_score
from backend.auth.utils.access_control import make_access_decision
from backend.auth.utils.access_logger import log_auth_attempt  
from backend.auth.utils.token_manager import verify_token

apps_blueprint = Blueprint('apps', __name__, template_folder='../../templates/apps')


@apps_blueprint.route('/simulate_app_login', methods=['GET', 'POST'])
def simulate_app_login():
    if request.method == 'POST':
        email = request.form.get('email')
        typing_data = request.form.get('typing_speed')

        # Token verification (optional)
        token = session.get('token')
        if not token or not verify_token(token):
            return redirect(url_for('auth.login'))

        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))

        # Context and risk
        context_data = collect_context_data(request, typing_data)
        risk_score = compute_risk_score(context_data, typing_data)  
        trust_score = update_trust_score(user_id, risk_score)
        decision = make_access_decision(risk_score, trust_score)

        log_auth_attempt(user_id, context_data, risk_score, trust_score, decision)  

        if decision == "allow":
            return render_template('apps/app_home.html', email=email)
        elif decision == "challenge":
            return render_template('auth/challenge.html', context=context_data)
        else:
            return render_template('auth/denied.html', reason="Risk too high.")

    return render_template('apps/app_login.html')


@apps_blueprint.route('/app_home')
def app_home():
    token = session.get('token')
    if not token or not verify_token(token):
        return redirect(url_for('auth.login'))

    return render_template('apps/app_home.html', email=session.get('email'))
