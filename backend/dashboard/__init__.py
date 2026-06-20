"""
Dashboard Module Setup
-------------------------
This module configures the admin dashboard functionality for the Hybrid Context-Aware IAM system.

Key Functions:
- Registers the dashboard blueprint to provide admin and user-level access logs, along with risk visibility.
- Facilitates real-time tracking of risk, trust, and access patterns.
- Supports modules for visualizing risk trends, anomaly scoring, and session timelines.
- Provides access to security logs, role/policy settings, and system analytics.

Significance:
The dashboard acts as the central hub for security administrators, offering insights, control, and analysis of user behavior, access decisions, and the dynamics between trust and risk.
"""


from flask import Blueprint

# blueprint for dashboard functionality
dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='../../templates/dashboard')

# import routes to bind views to this blueprint
from . import routes  # noqa: F401 – ensures route definitions are loaded and registered
