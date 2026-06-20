from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import jsonify
from werkzeug.security import check_password_hash
from backend.auth.utils.context_engine import collect_context_data
from backend.auth.utils.behavioral_model import analyze_behavior
from backend.ml.scoring import compute_risk_score
from backend.auth.utils.trust_engine import update_trust_score
from backend.auth.utils.access_logger import log_auth_attempt
from backend.auth.utils.token_manager import issue_token as create_session_token, revoke_token as revoke_session
from backend.auth.utils.db import get_user_by_email
from backend.auth.utils.helpers import make_access_decision
from backend.auth.utils.issue_vc import issue_credential, upload_to_ipfs
from backend.auth.utils.verify_vc import verify_credential

import datetime
import requests

auth_blueprint = Blueprint('auth', __name__, template_folder='../../templates/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #  reCAPTCHA Validation
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret_key = '6LcZ5S4rAAAAAL1eAwGp375XqnKh2025OSCEWX6Q'
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {'secret': secret_key, 'response': recaptcha_response}
        response = requests.post(verify_url, data=payload)
        result = response.json()

        if not result.get('success'):
            return render_template('auth/login.html', error="CAPTCHA validation failed. Please try again.")

        # extract form data
        email = request.form.get('email')
        password = request.form.get('password')
        typing_data = request.form.get('typing_durations') or "0"

        # authenticate user (fallback to passwordless)
        user = get_user_by_email(email)
        if not user:
            return render_template('auth/login.html', error="User not found")

        passwordless = not password

        if password and not check_password_hash(user.password_hash, password):
            return render_template('auth/login.html', error="Invalid password")

        #  Step 1: Context and Behavioral Analysis
        context_data = collect_context_data(request, typing_data)
        context_data['timestamp'] = str(datetime.datetime.utcnow())

        #  Step 2: Behavioral Score
        behavior_score = analyze_behavior(typing_data, typing_data)

        # Step 3: Risk & Trust Scoring
        risk_score = compute_risk_score(context_data, behavior_score)
        trust_score = update_trust_score(email, risk_score)

        # Force denial for user2@example.com (for demo)
        if email == "user2@example.com":
            risk_score = 0.85
            trust_score = 0.3
            print("[FORCE DENY] Overriding risk/trust for user2@example.com")

        print(f"[DEBUG] Passwordless: {passwordless}, Behavior: {behavior_score}, Risk: {risk_score}, Trust: {trust_score}")

        # Step 4: Extra Gate for Passwordless
        if passwordless:
            if risk_score >= 0.8:
                return render_template('auth/login.html', error="Passwordless login denied: high risk.")
            elif trust_score < 0.4:
                return render_template('auth/login.html', error="Passwordless login denied: low trust.")

        # Step 5: Access Decision
        decision = make_access_decision(risk_score, trust_score)

        # Diagnostic Logging
        print(f"[DEBUG] Typing Data: {typing_data}")
        print(f"[DEBUG] Behavior Score: {behavior_score}")
        print(f"[DEBUG] Risk Score: {risk_score}")
        print(f"[DEBUG] Trust Score: {trust_score}")
        print(f"[DEBUG] Final Access Decision: {decision}")

        #  Step 6: Log Attempt
        log_auth_attempt(
            user_id=email,
            timestamp=datetime.datetime.utcnow(),
            context=context_data,
            risk_score=risk_score,
            trust_score=trust_score,
            decision=decision,
            method="passwordless" if passwordless else "password"
        )

        # Step 7: Enforce Decision
        if decision == "allow":
            token = create_session_token(user_id=user.id, context=context_data)
            session['token'] = token
            session['user_id'] = user.id
            session['email'] = user.email
            session['role'] = user.role
            session['context'] = context_data
            session['risk_score'] = risk_score
            session['trust_score'] = trust_score
            session['decision'] = decision
            return redirect(url_for('dashboard.dashboard_home'))

        elif decision == "challenge":
            session['user_id'] = user.id
            session['email'] = user.email
            session['context'] = context_data
            session['risk_score'] = risk_score
            session['trust_score'] = trust_score
            session['decision'] = decision
            return render_template('auth/challenge.html', context=context_data)

        elif decision == "deny":
            return render_template('auth/denied.html', reason="High risk detected")

    return render_template('auth/login.html')

@auth_blueprint.route('/logout')
def logout():
    user_id = session.get('user_id')
    revoke_session(user_id=user_id)
    session.clear()
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/challenge', methods=['POST'])
def challenge():
    user_id = session.get('user_id')
    email = session.get('email')
    context_data = session.get('context', {})

    if not user_id or not email:
        return redirect(url_for('auth.login'))

    user = get_user_by_email(email)
    if not user:
        return redirect(url_for('auth.login'))

    token = create_session_token(user_id=user.id, context=context_data)
    session['token'] = token
    session['user_id'] = user.id
    session['email'] = user.email
    session['role'] = user.role
    session['context'] = context_data
    session['risk_score'] = session.get('risk_score', 0.0)
    session['trust_score'] = session.get('trust_score', 0.0)
    session['decision'] = session.get('decision', 'challenge')

    return redirect(url_for('dashboard.dashboard_home'))
@auth_blueprint.route("/issue_credential", methods=["POST"])
def api_issue_credential():
    data = request.get_json()
    did = data.get("did")
    email = data.get("email")
    role = data.get("role")

    if not all([did, email, role]):
        return jsonify({"error": "Missing fields"}), 400

    vc = issue_credential(did, email, role)
    ipfs_hash = upload_to_ipfs(vc)
    return jsonify({"vc": vc, "ipfs_hash": ipfs_hash}), 200

@auth_blueprint.route("/verify_credential", methods=["POST"])
def api_verify_credential():
    vc = request.get_json()
    if not vc:
        return jsonify({"error": "VC not provided"}), 400

    valid = verify_credential(vc)
    return jsonify({"valid": valid}), 200
@auth_blueprint.route("/vc", methods=["GET"])
def verifiable_credential_page():
    return render_template("auth/verifiable_credential.html")

from backend.auth.utils.policy_manager import get_policy_from_ipfs
from backend.ml.atfe import get_trust_score

@auth_blueprint.route("/admin/settings")
def admin_settings():
    user_did = session.get("user_id")
    user_vc = session.get("role")  # Simplified to session-stored role
    trust_score = session.get("trust_score", 0.5)

    # Replace this with your real policy hash (upload it via upload_policy.py)
    policy_hash = "QmReplaceWithYourPolicyHash"
    policy = get_policy_from_ipfs(policy_hash)

    # Match on resource and DID (optional strict check)
    if policy["resource"] != "/admin/settings":
        return render_template("auth/denied.html", reason="Policy resource mismatch")

    # Role check
    required_role = policy["conditions"].get("role")
    if required_role and session.get("role") != required_role:
        return render_template("auth/denied.html", reason="Insufficient role")

    # Trust score check
    min_trust = policy["conditions"].get("trust_score_min", 0.0)
    if trust_score < min_trust:
        return render_template("auth/denied.html", reason="Low trust score")

    return render_template("admin/settings.html")