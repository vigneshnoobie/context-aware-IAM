from flask import Blueprint

# Create blueprint
auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

# Importing routes and controllers in a way that avoids circular imports
from . import routes
from . import controllers
from backend.auth import utils
# Important Note:
# Do NOT import ML modules like risk_engine or scoring at the top level here.
# Instead, import them inside the functions within the controllers/routes when necessary.
# This approach helps avoid circular import issues.
