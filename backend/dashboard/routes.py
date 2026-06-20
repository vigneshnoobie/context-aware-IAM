from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from backend.auth.utils.access_logger import get_recent_logs
from backend.auth.utils.db import db, User

dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='../../templates/dashboard')


@dashboard_blueprint.route('/')
def dashboard_home():
    email = session.get('email')
    role = session.get('role', 'user')  
    context = session.get('context', {})
    scores = {
        "risk": session.get("risk_score", "N/A"),
        "trust": session.get("trust_score", 0.5)
    }
    decision = session.get("decision", "N/A")

    user = {"email": email}

    logs = {
        "forwarded": True
    }

    
    dummy_apps = [
        {"name": "Finance Portal", "url": "/app/finance"},
        {"name": "HR System", "url": "/app/hr"},
        {"name": "DevOps Dashboard", "url": "/app/devops"},
        {"name": "Project Tracker", "url": "/app/projects"},
        {"name": "Research Archive", "url": "/app/research"}
    ]

    return render_template(
        "auth/user_dashboard.html",
        session=session,
        context=context,
        scores=scores,
        decision=decision,
        user=user,
        role=role,
        logs=logs,
        apps=dummy_apps
    )


@dashboard_blueprint.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        abort(403)

    logs = get_recent_logs()

    federated = {
        'participants': 5,
        'last_aggregation': '2025-05-01 13:22',
        'status': 'Active'
    }

    policy = {
        'trust_threshold': 0.65,
        'risk_tolerance': 0.4
    }

    all_users = User.query.all()

    return render_template(
        "dashboard/admin_dashboard.html",
        logs=logs,
        federated=federated,
        policy=policy,
        all_users=all_users
    )


@dashboard_blueprint.route('/update_roles', methods=['POST'])
def update_roles():
    if session.get('role') != 'admin':
        abort(403)

    user_id = request.form.get('user')
    new_role = request.form.get('role')

    user = User.query.filter_by(id=user_id).first()
    if user:
        user.role = new_role
        db.session.commit()
        flash(f"Role updated for {user.email} to {new_role}.")
    else:
        flash("User not found.")

    return redirect(url_for('dashboard.admin_dashboard'))



@dashboard_blueprint.route('/app/<app_name>')
def dummy_app(app_name):
    user_role = session.get('role', 'user')
    trust_score = float(session.get('trust_score', 0.5))

    restricted_apps = {
        'finance': {'role': 'admin', 'min_trust': 0.8},
        'hr': {'role': 'user', 'min_trust': 0.6},
        'devops': {'role': 'admin', 'min_trust': 0.7},
        'projects': {'role': 'user', 'min_trust': 0.5},
        'research': {'role': 'guest', 'min_trust': 0.4}
    }

    app_key = app_name.lower()
    if app_key in restricted_apps:
        required = restricted_apps[app_key]
        if user_role != required['role'] or trust_score < required['min_trust']:
            return f"<h2>Access Denied to {app_name.title()}</h2><p>Your role or trust score is insufficient.</p>", 403

    return f"<h1>{app_name.title()}</h1><p>Welcome! Your access is granted.</p>"
