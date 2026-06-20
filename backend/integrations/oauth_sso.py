import os
import requests
from flask import Blueprint, redirect, request, session, url_for
from backend.auth.utils.context_engine import collect_context_data as collect_context
from backend.auth.utils.risk_model import compute_risk_score as evaluate_risk_score
from backend.auth.utils.trust_engine import update_trust_score
from backend.auth.utils.access_logger import log_auth_attempt  
from backend.ml.role_mapper import determine_role

sso_blueprint = Blueprint('sso', __name__, template_folder='templates/sso')


github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
github_auth_url = "https://github.com/login/oauth/authorize"
github_token_url = "https://github.com/login/oauth/access_token"
github_user_api = "https://api.github.com/user"


slack_client_id = os.getenv("SLACK_CLIENT_ID")
slack_client_secret = os.getenv("SLACK_CLIENT_SECRET")
slack_auth_url = "https://slack.com/oauth/v2/authorize"
slack_token_url = "https://slack.com/api/oauth.v2.access"
slack_user_api = "https://slack.com/api/users.identity"


@sso_blueprint.route('/sso/github')
def github_login():
    redirect_uri = url_for('sso.github_callback', _external=True)
    return redirect(f"{github_auth_url}?client_id={github_client_id}&redirect_uri={redirect_uri}&scope=read:user")


@sso_blueprint.route('/sso/github/callback')
def github_callback():
    code = request.args.get("code")
    if not code:
        return "GitHub login failed.", 400

    token_res = requests.post(github_token_url, headers={'Accept': 'application/json'}, data={
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    })
    access_token = token_res.json().get('access_token')
    if not access_token:
        return "GitHub token error.", 401

    user_res = requests.get(github_user_api, headers={"Authorization": f"token {access_token}"})
    user = user_res.json()
    username = user.get("login")
    user_id = f"github_{user.get('id')}"

    context = collect_context(request)
    context['provider'] = 'GitHub'

    risk_score = evaluate_risk_score(user_id, context)
    trust_score = update_trust_score(user_id, context, risk_score)
    role = determine_role(user, context, risk_score)

    log_auth_attempt(  
        user_id=user_id,
        context=context,
        risk_score=risk_score,
        trust_score=trust_score,
        decision="allow"
    )

    session['user_id'] = user_id
    session['username'] = username
    session['role'] = role
    session['trust'] = trust_score

    return redirect(url_for('dashboard.dashboard_home'))


@sso_blueprint.route('/sso/slack')
def slack_login():
    redirect_uri = url_for('sso.slack_callback', _external=True)
    return redirect(f"{slack_auth_url}?client_id={slack_client_id}&redirect_uri={redirect_uri}&scope=identity.basic")


@sso_blueprint.route('/sso/slack/callback')
def slack_callback():
    code = request.args.get("code")
    if not code:
        return "Slack login failed.", 400

    token_res = requests.post(slack_token_url, data={
        'client_id': slack_client_id,
        'client_secret': slack_client_secret,
        'code': code,
        'redirect_uri': url_for('sso.slack_callback', _external=True)
    })
    access_token = token_res.json().get('access_token')
    if not access_token:
        return "Slack token error.", 401

    user_res = requests.get(slack_user_api, headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_res.json()
    user = user_info.get('user', {})
    username = user.get('name')
    user_id = f"slack_{user.get('id')}"

    context = collect_context(request)
    context['provider'] = 'Slack'

    risk_score = evaluate_risk_score(user_id, context)
    trust_score = update_trust_score(user_id, context, risk_score)
    role = determine_role(user, context, risk_score)

    log_auth_attempt(  # 
        user_id=user_id,
        context=context,
        risk_score=risk_score,
        trust_score=trust_score,
        decision="allow"
    )

    session['user_id'] = user_id
    session['username'] = username
    session['role'] = role
    session['trust'] = trust_score

    return redirect(url_for('dashboard.dashboard_home'))