# Flask App (Optional UI Layer)

Flask UI complementing the FastAPI backend. Provides HTML dashboards, auth pages, and future realtime & admin surfaces.

## Structure

Directory highlights:

| Path | Purpose |
|------|---------|
| `flask_app/__init__.py` | App factory, auto-discovery of blueprints, extension wiring |
| `flask_app/config.py` | Environment-specific config (Development/Testing/Production) |
| `flask_app/blueprints/` | Modular features: `auth`, `dashboard`, `firebase_auth`, future `payments`, `chats` |
| `flask_app/services/` | Business logic layer (pricing, order processing stubs) |
| `flask_app/utils/` | Reusable helpers (pagination, response builders) |
| `flask_app/exceptions.py` | Domain exceptions mapped to error handlers |
| `flask_app/error_handlers.py` | Centralized JSON error responses |
| `flask_app/templates/` | Jinja2 templates |
| `flask_app/static/` | CSS & JS assets (bundled via Flask-Assets) |
| `flask_app/requirements.txt` | Dependencies including CORS, rate limiting, validation |
| `.env.example` | Sample environment variables |

## Run (Development)

Create a virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r flask_app/requirements.txt

# (Optional) install dev tools like ruff/black if separated:
pip install ruff black
```

Export environment variables and run:

```bash
export FLASK_APP=flask_app
export FLASK_ENV=development
export FLASK_SECRET_KEY="replace-with-long-random"  # MUST change for production
export APP_VERSION="0.1.0"
export CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
flask run --debug
```

Open http://127.0.0.1:5000/dashboard/

Health JSON (includes version):

```bash
curl http://127.0.0.1:5000/api/v1/health
```

## Assets (CSS/JS Bundling)

This scaffold uses Flask-Assets (webassets) for bundle + minify.

### Bundles
- `main_css`: `css/app.css` -> `gen/app.min.css`
- `main_js`: `js/app.js` -> `gen/app.min.js`

### Development
By default, bundle tags will render the processed asset. For rapid iteration you can still reference raw files by disabling assets (comment out `register_assets(app)` in `__init__.py`).

### Production Build
Pre-build the bundles so they are served as static files:

```bash
export FLASK_APP=flask_app
flask assets build
```

This will write minified files to `static/gen/`. Ensure your deployment (reverse proxy) sets proper cache headers (immutable + long max-age) for `gen/*.min.*` files.

### Per-page Scripts
Place page-specific JavaScript inside `{% block scripts %}` in individual templates to avoid polluting the global bundle.

Example:

```html
{% block scripts %}
	<script>
		// Page-specific logic
		console.log('Dashboard enhancements');
	</script>
{% endblock %}
```

### Adding More Files
Append to bundles in `flask_app/assets.py`:

```python
main_css.contents += ("css/extra.css", )
main_js.contents += ("js/extra.js", )
```

Then rebuild.

## Validation / Security / Observability Roadmap

Planned / partial:

- Firebase ID token verification (`firebase_auth` blueprint) optional if credentials present.
- Rate limiting (Flask-Limiter) per IP: auth endpoints (5/min), default (100/min).
- CORS whitelist from `CORS_ORIGINS`.
- Marshmallow schemas for payload validation.
- Uniform JSON error format `{"error": {"code": int, "message": str, "detail": optional}}`.
- Metrics placeholder `/api/v1/metrics` for Prometheus integration later.
- Pagination helper ensures consistent metadata (`page`, `per_page`, `total`).

## Contributing

1. Copy `.env.example` to `.env` and fill secrets.
2. Ensure `SECRET_KEY` is 32+ random characters for production.
3. Run lint: `ruff check flask_app/` (optional pre-commit hook).

## Security

See `SECURITY.md` for reporting guidelines.
