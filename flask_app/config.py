import os


class BaseConfig:
    """Base configuration shared by all environments.

    NOTE: SECRET_KEY must be overridden in production via environment variable.
    """

    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-key")  # GANTI di produksi
    FIREBASE_CREDENTIALS_JSON = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    APP_VERSION = os.environ.get("APP_VERSION", "0.1.0")
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True
    RATELIMIT_HEADERS_ENABLED = True

    # Flask / SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "FLASK_SQLALCHEMY_DATABASE_URI", "sqlite:///instance/app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    # Static/template folders (Flask will use these when app is created)
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    # Often in tests we disable CSRF & ratelimit headers to simplify form submissions
    WTF_CSRF_ENABLED = False
    RATELIMIT_HEADERS_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = False  # Rely on error handlers / logging infra


def get_config() -> type[BaseConfig]:
    """Return the appropriate config class based on FLASK_ENV.

    FLASK_ENV values: production | testing | development (default)
    """
    env = os.environ.get("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    if env == "testing":
        return TestingConfig
    return DevelopmentConfig
