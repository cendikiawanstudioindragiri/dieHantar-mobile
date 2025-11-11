from flask import Flask
import os

from .extensions import db, csrf, assets_env
from .assets import main_css, main_js
from .blueprints import discover_blueprints
from .error_handlers import register_error_handlers
from flask_cors import CORS
from .logger_config import configure_logging
from .limiting import limiter


def create_app(config_object: str | None = None) -> Flask:
    """Application factory.

    If `config_object` is None, will resolve an environment-specific config
    using `flask_app.config.get_config()`. Otherwise expects dotted path string
    or direct class reference.
    """
    app = Flask(__name__, instance_relative_config=True)
    if config_object is None:
        from .config import get_config
        app.config.from_object(get_config())
    else:
        app.config.from_object(config_object)

    configure_logging()
    register_extensions(app)
    register_blueprints(app)
    register_jinja_globals(app)
    register_assets(app)
    register_error_handlers(app)

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    csrf.init_app(app)
    # CORS
    origins = (app.config.get("CORS_ORIGINS") or os.getenv("CORS_ORIGINS") or "").split(",")
    cleaned = [o.strip() for o in origins if o.strip()]
    if cleaned:
        CORS(app, origins=cleaned, supports_credentials=True)
    else:
        CORS(app)

    # Rate Limiter
    default_limit = os.getenv("RATE_LIMIT_DEFAULT", "100/minute")
    auth_limit = os.getenv("RATE_LIMIT_AUTH", "5/minute")
    limiter.init_app(app, default_limits=[default_limit])
    # Store for reuse (e.g., decorators)
    app.limiter = limiter  # type: ignore[attr-defined]
    app.config["RATE_LIMIT_AUTH"] = auth_limit


def register_blueprints(app: Flask) -> None:
    """Auto-register all discovered blueprints.

    Each blueprint may optionally define `URL_PREFIX` in its module to
    customize prefix; fallback is `/{bp.name}`.
    """
    for bp in discover_blueprints():
        # Attempt to fetch custom prefix from its module
        module = bp.import_name  # module path used when blueprint created
        prefix = f"/{bp.name}"
        try:
            mod = __import__(module, fromlist=["URL_PREFIX"])
            custom = getattr(mod, "URL_PREFIX", None)
            if isinstance(custom, str):
                prefix = custom
        except Exception:  # pragma: no cover
            pass
        app.register_blueprint(bp, url_prefix=prefix)


def register_jinja_globals(app: Flask) -> None:
    # Enables {% break %} and {% continue %} in templates
    app.jinja_env.add_extension("jinja2.ext.loopcontrols")


def register_assets(app: Flask) -> None:
    # Lazy import to avoid optional dependency during non-asset usage
    from flask_assets import Environment

    global assets_env
    assets_env = Environment(app)
    # Tell webassets where the static directory is
    assets_env.directory = app.static_folder
    assets_env.url = app.static_url_path
    # Register bundles
    assets_env.register("main_css", main_css)
    assets_env.register("main_js", main_js)
