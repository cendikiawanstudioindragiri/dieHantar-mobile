from __future__ import annotations

from fastapi import APIRouter
from app.core.config import settings


router = APIRouter(prefix="/config", tags=["config"])


@router.get("/splash")
def splash_config():
    return {
        "image": "https://cdn.example.com/splash/default.png",
        "duration_ms": 1500,
        "min_version": "1.0.0",
    }


@router.get("/popup")
def popup_config():
    return {
        "title": "Promo Akhir Tahun",
        "body": "Diskon hingga 50% untuk pengguna baru!",
        "cta": {"label": "Lihat", "url": "/promos"},
        "schedule": {"start": "2025-12-01T00:00:00Z", "end": "2025-12-31T23:59:59Z"},
        "target": {"segment": "new_users"},
        "frequency": {"per_day": 1, "max_total": 3},
    }


@router.get("/greetings")
def greetings_config():
    return {
        "first_time": "Selamat datang di dieHantar!",
        "returning": "Senang bertemu lagi!",
    }


@router.get("/ads")
def ads_config():
    return {
        "slots": [
            {"id": "home_top", "priority": 10, "image": "https://cdn.example.com/ads/home_top.png", "target": {}},
            {"id": "search_banner", "priority": 5, "image": "https://cdn.example.com/ads/search.png", "target": {"segment": "active"}},
        ]
    }


@router.get("/map")
def map_config():
    return {
        "provider": "mapbox",
        "api_key": "${MAPBOX_PUBLIC_KEY}",
    }


@router.get("/app/{app_name}")
def app_config(app_name: str):
    base = {"min_version": "1.0.0", "feature_flags": settings.FEATURE_FLAGS}
    if app_name == "driver":
        base.update({"changelog": "- Perbaikan bug\n- Peningkatan stabilitas"})
    elif app_name == "merchant":
        base.update({"menu_sync_interval": 300})
    elif app_name == "admin":
        base.update({"modules": ["users", "orders", "reports"]})
    return base


@router.get("/brand")
def brand_config():
    return {"name": "dieHantar", "logo": "https://cdn.example.com/brand/logo.png", "colors": {"primary": "#004AAD"}}


@router.get("/capabilities")
def capabilities():
    return {
        "api_version": 1,
        "features": settings.FEATURE_FLAGS,
        "endpoints": [
            "/auth/login",
            "/products",
            "/categories",
            "/wallet/balance",
            "/config/splash",
            "/config/brand",
        ],
    }
