from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.api.auth import router as auth_router
from app.api.register import router as register_router
from app.api.me import router as me_router
from app.api.categories import router as categories_router
from app.api.products import router as products_router
from app.api.wallet import router as wallet_router
from app.api.configs import router as configs_router
from app.api.admin_broadcasts import router as broadcasts_router
from app.api.drivers import router as drivers_router

app = FastAPI(title="dieHantar API")
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Ensure SQLAlchemy model classes are registered for relationship resolution
from app.models import user as _user  # noqa: F401
from app.models import category as _category  # noqa: F401
from app.models import product as _product  # noqa: F401
from app.models import location as _location  # noqa: F401
from app.models import order as _order  # noqa: F401
from app.models import order_item as _order_item  # noqa: F401
from app.models import driver as _driver  # noqa: F401
from app.models import payment as _payment  # noqa: F401
from app.models import review as _review  # noqa: F401


@app.on_event("startup")
def startup_create_tables():
    """Import models to register mappers; optionally create tables for dev."""
    import os

    # Always import models so SQLAlchemy can resolve string-based relationships
    from app.models import (
        user as _user,  # noqa: F401
        category as _category,  # noqa: F401
        product as _product,  # noqa: F401
        location as _location,  # noqa: F401
        order as _order,  # noqa: F401
        order_item as _order_item,  # noqa: F401
        driver as _driver,  # noqa: F401
        payment as _payment,  # noqa: F401
        review as _review,  # noqa: F401
    )
    from sqlalchemy.orm import configure_mappers
    # Ensure relationships are fully resolved at startup
    configure_mappers()

    # For production/migrations we rely on Alembic; keep create_all only if env var DEV_AUTO_CREATE=1
    if os.getenv("DEV_AUTO_CREATE", "0") == "1":
        from app.db.session import Base, engine  # local import to avoid circulars
        Base.metadata.create_all(bind=engine)

# get_db moved to app.db.session

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the dieHantar API!"}

@app.get("/health", tags=["health"])
def health(db: Session = Depends(get_db)):
    # simple check executing a lightweight query
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "degraded", "error": str(e)}


app.include_router(auth_router, tags=["Authentication"])
app.include_router(register_router, tags=["Authentication"])
app.include_router(me_router, tags=["Authentication"])
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(wallet_router)
app.include_router(configs_router)
app.include_router(broadcasts_router)
app.include_router(drivers_router)

# Structured error & logging middleware (basic implementation)
import logging, time, uuid

logger = logging.getLogger("api")

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    rid = str(uuid.uuid4())
    start = time.time()
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = int((time.time() - start) * 1000)
        logger.info(
            {
                "request_id": rid,
                "method": request.method,
                "path": request.url.path,
                "status_code": getattr(response, "status_code", 500),
                "duration_ms": duration_ms,
            }
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": exc.detail}},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"error": {"code": 500, "message": "Internal server error"}},
    )
