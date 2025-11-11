from __future__ import annotations

from flask import Blueprint, Response

bp = Blueprint("metrics", __name__, url_prefix="")


@bp.route("/metrics", methods=["GET"])
def metrics():
    # Placeholder metrics to avoid hard dependency on prometheus_client
    body = "# HELP app_placeholder_metric Always 1 as a placeholder\n# TYPE app_placeholder_metric gauge\napp_placeholder_metric 1\n"
    return Response(body, status=200, mimetype="text/plain; version=0.0.4")
