"""Blueprint package initializer with auto-discovery utilities.

Expose a function `discover_blueprints()` that imports all modules in this
package searching for a top-level variable named `bp` which is assumed to be
an instance of `flask.Blueprint`. This allows new blueprints to be added by
simply creating a file inside this directory.

Usage in app factory:
	from flask_app.blueprints import discover_blueprints
	for bp in discover_blueprints():
		app.register_blueprint(bp, url_prefix=f"/{bp.name}")  # or custom

Blueprint modules can override the default prefix by defining `URL_PREFIX`.
If present and is a string, it will be used instead of `/{bp.name}`.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from types import ModuleType
from typing import Iterator

from flask import Blueprint

PACKAGE_NAME = __name__
PACKAGE_PATH = Path(__file__).parent


def _iter_modules() -> Iterator[str]:
	"""Yield fully-qualified module names for python files in this package."""
	for info in pkgutil.iter_modules([str(PACKAGE_PATH)]):
		if info.ispkg:
			continue
		# skip private / dunder style modules
		if info.name.startswith("_"):
			continue
		yield f"{PACKAGE_NAME}.{info.name}"


def discover_blueprints() -> list[Blueprint]:
	"""Discover and import all blueprint modules returning collected blueprints.

	A module contributes if it defines a top-level variable named `bp` that is
	a `Blueprint` instance. Duplicate blueprint names are ignored (first wins).
	"""
	discovered: list[Blueprint] = []
	seen_names: set[str] = set()
	for module_name in _iter_modules():
		try:
			mod: ModuleType = importlib.import_module(module_name)
		except Exception:  # pragma: no cover - avoid breaking startup
			continue
		bp = getattr(mod, "bp", None)
		if isinstance(bp, Blueprint):
			if bp.name in seen_names:
				continue
			discovered.append(bp)
			seen_names.add(bp.name)
	return discovered

