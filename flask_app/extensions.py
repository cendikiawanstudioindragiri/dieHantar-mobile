from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_assets import Environment

# SQLAlchemy database instance
# Configure URI via Config class (SQLALCHEMY_DATABASE_URI)
db = SQLAlchemy()

# CSRF protection (use with Flask-WTF forms)
csrf = CSRFProtect()

# Flask-Assets environment (initialized in app factory)
assets_env: Environment | None = None
