import os
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from backend.auth.routes import auth_blueprint
from backend.dashboard.routes import dashboard_blueprint
from backend.apps.routes import apps_blueprint
from backend.integrations.oauth_sso import sso_blueprint
from backend.auth.utils.db import init_db
from backend.auth.utils.si_em import forward_logs_to_siem

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # App Configs
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default-secret')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # seconds (1 hour)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    CORS(app)
    JWTManager(app)
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(dashboard_blueprint, url_prefix='/')  
    app.register_blueprint(apps_blueprint, url_prefix='/apps')
    app.register_blueprint(sso_blueprint, url_prefix='/sso')

    # Forward logs to SIEM after every request
    @app.after_request
    def log_and_forward(response):
        forward_logs_to_siem(request, response)
        return response

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
